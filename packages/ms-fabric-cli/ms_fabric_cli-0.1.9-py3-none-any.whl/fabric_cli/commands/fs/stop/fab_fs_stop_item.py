# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_mirroring as mirroring_api
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import Item
from fabric_cli.core.fab_types import ItemType


# Items - Mirrored Database
def exec(item: Item, args: Namespace, force_start: bool) -> None:
    args.ws_id = item.get_workspace_id()
    args.id = item.get_id()
    args.name = item.get_name()

    # Only stop if DB running
    # status: Initialized, Initializing, Running, Starting, Stopped, Stopping

    response = mirroring_api.get_mirroring_status(args)
    if response.status_code == 200:
        state = json.loads(response.text)["status"]
        if state not in ("Running"):
            raise FabricCLIError(
                f"'{args.name}' is not in a valid state to stop. State: {state}",
                fab_constant.ERROR_NOT_RUNNING,
            )

    if item.get_item_type() == ItemType.MIRRORED_DATABASE:
        mirroring_api.stop_mirroring(args, force_start)
