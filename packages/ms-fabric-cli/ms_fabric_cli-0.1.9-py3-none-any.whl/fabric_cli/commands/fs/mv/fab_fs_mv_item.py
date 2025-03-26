# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_item as item_api
from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.core.fab_commands import Command
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import Item, ItemType, Workspace
from fabric_cli.utils import fab_mem_store as utils_mem_store
from fabric_cli.utils import fab_ui as utils_ui
from fabric_cli.utils import fab_util as utils


def move_bulk_items(
    from_context: Workspace,
    to_context: Workspace,
    args: Namespace,
    delete_from_item: Optional[bool] = True,
) -> None:

    ws_items: list[Item] = utils_mem_store.get_workspace_items(from_context)
    if not ws_items:
        raise FabricCLIError(
            f"Your workspace is empty",
            fab_constant.ERROR_INVALID_OPERATION,
        )

    # Only filter those items supporting definition
    supported_items = []
    for item in ws_items:
        try:
            if item.check_command_support(Command.FS_EXPORT):
                supported_items.append(item)
        except Exception:
            False

    if not supported_items:
        raise FabricCLIError(
            "Not possible. Your workspace items don't support definition",
            fab_constant.ERROR_NOT_SUPPORTED,
        )

    # Sort output by config
    sorted_supported_items = utils.sort_items_by_config(supported_items)

    if args.all:
        selected_items = [item.get_name() for item in sorted_supported_items]
    else:
        selected_items = utils_ui.prompt_select_items(
            "Select items:",
            [item.get_name() for item in sorted_supported_items],
        )

    if selected_items:
        utils_ui.print_grey("\n".join(selected_items))
        utils_ui.print_grey("------------------------------")
        filtered_items = [
            item for item in supported_items if item.get_name() in selected_items
        ]

        if args.force or utils_ui.prompt_confirm():

            successful_moves = 0
            from_workspace_path = args.from_path
            to_workspace_path = args.to_path

            for item in filtered_items:

                name = item.get_name().split(".")[0]
                new_item = Item(name, None, to_context, str(item.get_item_type()))
                args.force = True
                args.from_path = f"{from_workspace_path}/{item.get_name()}"
                args.to_path = f"{to_workspace_path}/{item.get_name()}"

                if move_single_item(
                    item, new_item, args, delete_from_item=delete_from_item
                ):
                    successful_moves = successful_moves + 1

            utils_ui.print("")
            utils_ui.print_done(
                f"{successful_moves} items {'moved' if delete_from_item else 'copied'} successfully"
            )


def move_single_item(
    from_context: Item,
    to_context: Item,
    args: Namespace,
    delete_from_item: Optional[bool] = True,
) -> bool:
    # Check supported for mv or if it's a Lakehouse.
    # A Lakehouse is whitelisted to support underlying OneLake move and copy operations
    if (
        not from_context.check_command_support(Command.FS_MV)
        or from_context.get_item_type() == ItemType.LAKEHOUSE
    ):
        raise FabricCLIError(
            fab_constant.WARNING_NOT_SUPPORTED_ITEM, fab_constant.ERROR_NOT_SUPPORTED
        )

    args.ws_id_from, args.ws_id_to = (
        from_context.get_workspace_id(),
        to_context.get_workspace_id(),
    )

    ws_items_target: list[Item] = utils_mem_store.get_workspace_items(
        to_context.get_parent()
    )

    # Move with definition (across workspaces supported)
    try:
        if _confirm_move(args.force):
            utils_ui.print_grey(
                f"{'Moving' if delete_from_item else 'Copying'} '{args.from_path}' → '{args.to_path}'..."
            )
            if any(
                target_item.get_name() == to_context.get_name()
                for target_item in ws_items_target
            ):
                if not args.force:
                    fab_logger.log_error(
                        f"Item already exists: '{to_context.get_name()}'",
                        fab_constant.ERROR_ALREADY_EXISTS,
                    )
                    return False

                # item_already_items = True

            # Move including definition, cross ws
            _move_item_with_definition(args, from_context, to_context, delete_from_item)
            return True
        else:
            return False
    except FabricCLIError as e:
        raise e


# Utils
def _confirm_move(bypass_confirmation: bool) -> bool:
    if not bool(bypass_confirmation):
        return utils_ui.prompt_confirm()
    return True


def _move_item_with_definition(
    args: Namespace,
    from_item: Item,
    to_item: Item,
    delete_from_item: Optional[bool],
    definition: Optional[bool] = True,
    item_already_items: Optional[bool] = False,
) -> None:

    # Obtain the source
    args.id = from_item.get_id()
    args.ws_id = from_item.get_workspace_id()
    if definition:
        args.format = ""
        item = item_api.get_item_withdefinition(args)
        payload = json.dumps(
            {
                "type": str(from_item.get_item_type()),
                "description": item["description"],
                "displayName": to_item.get_short_name(),
                "definition": item["definition"],
            }
        )

    # Create in target
    args.method = "post"
    args.ws_id = to_item.get_workspace_id()
    args.item_type = str(to_item.get_type())
    response = item_api.create_item(args, payload=payload)

    if response.status_code in (200, 201, 202):
        args.ws_id = from_item.get_workspace_id()

        if delete_from_item:
            args.uri = None  # empty URI to delete item since it can be completed by a LRO response
            item_api.delete_item(args, bypass_confirmation=True, debug=False)
            # Remove from mem_store
            utils_mem_store.delete_item_from_cache(from_item)

        data = json.loads(response.text)
        to_item._id = data["id"]

        # Add new one to mem_store
        utils_mem_store.upsert_item_to_cache(to_item)

        if definition:
            utils_ui.print_done(f"{'Move' if delete_from_item else 'Copy'} completed")
