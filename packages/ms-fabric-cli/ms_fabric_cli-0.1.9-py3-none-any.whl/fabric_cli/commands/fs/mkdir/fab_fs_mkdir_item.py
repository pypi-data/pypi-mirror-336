# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_item as item_api
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import Item
from fabric_cli.core.fab_types import format_mapping
from fabric_cli.utils import fab_cmd_mkdir_utils as mkdir_utils
from fabric_cli.utils import fab_mem_store as utils_mem_store
from fabric_cli.utils import fab_ui as utils_ui
from fabric_cli.utils import fab_util as utils


def exec(item: Item, args: Namespace) -> str | None:
    # Params
    params = args.params
    required_params, optional_params = mkdir_utils.get_params_per_item_type(item)

    if mkdir_utils.show_params_desc(
        params,
        item.get_item_type(),
        required_params=required_params,
        optional_params=optional_params,
    ):
        return None

    if item.get_id() is not None:
        raise FabricCLIError(
            "An item with the same name exists", fab_constant.ERROR_ALREADY_EXISTS
        )

    # Check required params
    mkdir_utils.check_required_params(params, required_params)

    args.ws_id = item.get_workspace_id()
    item_name = item.get_short_name()
    item_type = item.get_item_type()

    utils_ui.print_grey(f"Creating a new {item_type}...")
    args.item_type = str(item_type).lower()

    # Remove all unwanted keys from the params
    utils.remove_keys_from_dict(params, ["displayname", "type"])

    payload = {
        "description": "Created by fab",
        "displayName": item_name,
        "type": str(item_type),
    }
    payload = mkdir_utils.add_type_specific_payload(item, args, payload)
    json_payload = json.dumps(payload)
    args.item_uri = format_mapping.get(item.get_item_type(), "items")

    response = item_api.create_item(args, json_payload, item_uri=True)
    if response.status_code in (200, 201):
        utils_ui.print_done(f"'{item.get_name()}' created")
        data = json.loads(response.text)
        if data is not None and data.get("id"):
            _item_id = data["id"]
            item._id = _item_id
            # Update the cache with the new item
            utils_mem_store.upsert_item_to_cache(item)
            return _item_id
        else:
            # If the response does not contain an id, invalidate the cache
            utils_mem_store.invalidate_item_cache(item.get_workspace())
            return None
    return None
