# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import os
from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_onelake as onelake_api
from fabric_cli.client import fab_api_shortcuts as shortcut_api
from fabric_cli.core.fab_hiearchy import OneLakeItem
from fabric_cli.core.fab_types import OneLakeItemType
from fabric_cli.utils import fab_util as utils


# OneLake - Shortcut, File and Folder
def shortcut_file_or_folder(
    onelake: OneLakeItem,
    args: Namespace,
    force_delete: bool,
    debug: Optional[bool] = True,
) -> None:
    # Remove shortcut
    if onelake.get_nested_type() == OneLakeItemType.SHORTCUT:
        args.ws_id = onelake.get_workspace_id()
        args.id = onelake.get_item_id()
        args.path, args.sc_name = os.path.split(onelake.get_local_path().rstrip("/"))
        args.name = onelake.get_full_name()  # the name that is displayed in the UI

        shortcut_api.delete_shortcut(args, force_delete, debug)
        return

    # Remove file or folder
    path_name = utils.process_nargs(args.path)
    path_id = onelake.get_path_id().strip("/")

    args.directory = path_id
    args.name = path_name

    onelake_api.delete_dir(args, force_delete, debug)
