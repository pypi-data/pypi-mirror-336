# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.client import fab_api_item as item_api
from fabric_cli.core.fab_hiearchy import Item
from fabric_cli.utils import fab_mem_store as utils_mem_store


def exec(item: Item, args: Namespace, force_delete: bool) -> None:
    args.ws_id = item.get_workspace_id()
    args.id = item.get_id()
    args.name = item.get_name()
    args.item_type = item.get_type().value

    if item_api.delete_item(args, force_delete):
        # Remove from mem_store
        utils_mem_store.delete_item_from_cache(item)
