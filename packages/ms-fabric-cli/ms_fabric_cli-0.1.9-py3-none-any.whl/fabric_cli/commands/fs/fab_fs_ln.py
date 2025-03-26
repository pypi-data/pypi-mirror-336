# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
import os
from argparse import Namespace

from fabric_cli.client import fab_api_shortcuts as shortcut_api
from fabric_cli.core import fab_constant
from fabric_cli.core import fab_handle_context as handle_context
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import OneLakeItem
from fabric_cli.core.fab_types import ItemType
from fabric_cli.utils import fab_cmd_ln_utils as utils_ln
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: OneLakeItem) -> None:
    if args.force or utils_ui.prompt_confirm():
        args.directory = context.get_path()
        args.ws_id = context.get_workspace_id()
        args.id = context.get_item_id()
        args.shortcutConflictPolicy = "GenerateUniqueName" if args.force else "Abort"

        if not context.get_parent().get_item_type() == ItemType.LAKEHOUSE:
            raise FabricCLIError(
                fab_constant.WARNING_ONLY_SUPPORTED_WITHIN_LAKEHOUSE,
                fab_constant.ERROR_INVALID_PATH,
            )

        if not context.get_local_path().lower().startswith(
            "files/"
        ) and not context.get_local_path().lower().startswith("tables/"):
            raise FabricCLIError(
                fab_constant.WARNING_ONLY_SUPPORTED_WITHIN_FILES_AND_TABLES,
                fab_constant.ERROR_INVALID_PATH,
            )

        if not context.get_local_path().lower().endswith(".shortcut"):
            raise FabricCLIError(
                "Invalid path. The path must end with '.Shortcut'",
                fab_constant.ERROR_INVALID_PATH,
            )

        full_path, _ = os.path.splitext(context.get_local_path())

        if (args.target is not None and args.input is not None) or (
            args.target is None and args.input is None
        ):
            raise FabricCLIError(
                "Invalid arguments. Exactly one of --target or --input is required",
                fab_constant.ERROR_INVALID_INPUT,
            )

        if args.type != "oneLake" and args.target is not None:
            raise FabricCLIError(
                "Invalid arguments. --target is only supported for oneLake",
                fab_constant.ERROR_INVALID_INPUT,
            )

        args.path, args.name = os.path.split(full_path.rstrip("/"))

        utils_ln.validate_shortcut_name(args.name)

        if args.target is not None:
            _create_shortcut_from_target(args)
        else:
            utils_ln.parse_json(args)
            try:
                target_json = json.loads(args.target_json)
            except json.JSONDecodeError:
                raise FabricCLIError(
                    fab_constant.WARNING_INVALID_JSON_FORMAT,
                    fab_constant.ERROR_INVALID_JSON,
                )
            _create_shortcut_from_json(args, target_json)


def _create_shortcut_from_target(args: Namespace) -> None:
    target_context = handle_context.get_command_context(args.target)

    workspace_id = target_context.get_workspace_id()
    item_id = target_context.get_item_id()
    target_path = target_context.get_local_path()

    target_json = {"workspaceId": workspace_id, "itemId": item_id, "path": target_path}

    _create_shortcut_from_json(args, target_json)


def _create_shortcut_from_json(args: Namespace, target_json: dict) -> None:
    payload = {
        "path": args.path,
        "name": args.name,
        "target": {args.type: target_json},
    }
    utils_ui.print_grey("Creating a new Shortcut...")
    response = shortcut_api.create_shortcut(args, payload)

    if response.status_code in (200, 201):
        utils_ui.print_done(f"'{args.name}.Shortcut' created")
