# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from typing import Any, Dict

from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import OneLakeItem
from fabric_cli.core.fab_types import OneLakeItemType


def add_table_props_to_args(args: Any, context: OneLakeItem) -> None:
    if not isinstance(context, OneLakeItem):
        raise FabricCLIError(
            "Invalid path. Please provide a valid table path",
            fab_constant.ERROR_INVALID_PATH,
        )
    args.ws_id = context.get_workspace_id()
    args.lakehouse_id = context.get_item_id()
    args.item_type = str(context.get_item_type())
    args.lakehouse_path = context.get_item().get_path()

    table_path = context.get_local_path().split("/")
    # TODO improve underlying delta_log checking and proper error
    # Check if the path starts with "Tables" and has exactly 2 (Tables/table) or 3 components (Tables/schema/table)
    # if context.get_nested_type() not in [
    #     OneLakeItemType.TABLE,
    #     OneLakeItemType.SHORTCUT,
    # ]:
    #     raise FabricCLIError(
    #         f"Invalid path. Please provide a valid table path",
    #         fab_constant.ERROR_INVALID_PATH,
    #     )
    args.table_name = table_path[-1]
    args.schema = table_path[-2] if len(table_path) == 3 else None


def convert_hours_to_dhhmmss(hours: int) -> str:
    hours = int(hours)
    days = hours // 24
    hours_left = hours % 24
    minutes = 0
    seconds = 0
    return f"{days}:{hours_left:02}:{minutes:02}:{seconds:02}"


def parse_table_format_argument(format_arg: str) -> dict:
    allowed_keys = {"format", "header", "delimiter"}
    parsed_values = {}

    for part in format_arg.split(","):
        part = part.strip()
        if not part:
            continue  # Skip empty parts

        if "=" not in part:
            raise FabricCLIError(f"Invalid format argument: '{part}' (missing '=')")

        k, v = part.split("=", 1)
        k, v = k.strip(), v.strip()

        if k not in allowed_keys:
            raise FabricCLIError(
                f"Invalid key: '{k}'. Allowed keys are: {allowed_keys}"
            )

        # Strip quotes if present
        if (v.startswith("'") and v.endswith("'")) or (
            v.startswith('"') and v.endswith('"')
        ):
            v = v[1:-1]

        # Convert 'true' and 'false' to boolean
        parsed_values[k] = v.lower() == "true" if v.lower() in {"true", "false"} else v

    return parsed_values
