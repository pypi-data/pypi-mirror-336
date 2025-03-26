# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace
from typing import Any

from fabric_cli.client import fab_api_onelake as onelake_api
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import OneLakeItem
from fabric_cli.core.fab_types import (
    ItemOnelakeWritableFoldersMap,
    ItemType,
    OneLakeItemType,
)
from fabric_cli.utils import fab_ui as utils_ui


def upload_file_onelake(args: Namespace, content: Any) -> None:
    response = onelake_api.touch_file(args)
    if response.status_code == 201:
        # Infer the content type from the file extension
        content_type = _infer_content_type(args.to_path)
        onelake_api.append_file(args, content, 0, content_type)
        onelake_api.flush_file(args, len(content))
        utils_ui.print_done("Done")


def get_file_content_onelake(args: Namespace) -> str:
    response = onelake_api.get(args)
    return response.text


def get_onelake_file_destination(
    to_context: OneLakeItem, sourceFileName: str
) -> OneLakeItem:
    # If the destination is a folder or shortcut, update the context to a new file inside the folder with the same name as the source
    if to_context.get_nested_type() in [
        OneLakeItemType.SHORTCUT,
        OneLakeItemType.FOLDER,
    ]:
        to_context = OneLakeItem(
            sourceFileName,
            to_context.get_id(),
            to_context,
            OneLakeItemType.FILE,
        )
        return to_context
    # If the destination is a file or not exists (undefined and no id), return the context as is
    elif to_context.get_nested_type() == OneLakeItemType.FILE or (
        to_context.get_nested_type() == OneLakeItemType.UNDEFINED
        and to_context.get_id() is None
    ):
        return to_context

    raise FabricCLIError(
        "Invalid destination, expected file or writable folder",
        fab_constant.ERROR_INVALID_PATH,
    )


def check_onelake_destination(to_context: OneLakeItem) -> None:
    item_type: ItemType = to_context.get_item_type()
    root_folder = to_context.get_root_folder()
    supported_folders = ItemOnelakeWritableFoldersMap[item_type]

    if root_folder not in supported_folders:
        raise FabricCLIError(
            f"Cannot write in folder '{root_folder}' for {item_type}. Only {supported_folders} folders are supported",
            fab_constant.ERROR_NOT_SUPPORTED,
        )


# Utils
def _infer_content_type(file_path: str) -> str:
    """Infer the content type from the file extension."""
    if file_path.endswith(".json"):
        return "application/json"
    elif file_path.endswith(".csv"):
        return "text/csv"
    elif file_path.endswith(".txt"):
        return "text/plain"
    else:
        return "application/octet-stream"
