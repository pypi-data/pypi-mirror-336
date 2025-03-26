# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs.get import fab_fs_get_capacity as get_capacity
from fabric_cli.commands.fs.get import fab_fs_get_connection as get_connection
from fabric_cli.commands.fs.get import fab_fs_get_domain as get_domain
from fabric_cli.commands.fs.get import (
    fab_fs_get_externaldatashare as get_externaldatashare,
)
from fabric_cli.commands.fs.get import fab_fs_get_gateway as get_gateway
from fabric_cli.commands.fs.get import fab_fs_get_item as get_item
from fabric_cli.commands.fs.get import (
    fab_fs_get_managedprivateendpoint as get_managedprivateendpoint,
)
from fabric_cli.commands.fs.get import fab_fs_get_onelake as get_onelake
from fabric_cli.commands.fs.get import fab_fs_get_sparkpool as get_sparkpool
from fabric_cli.commands.fs.get import fab_fs_get_workspace as get_workspace
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_hiearchy import (
    FabricElement,
    Item,
    OneLakeItem,
    VirtualItem,
    VirtualWorkspaceItem,
    Workspace,
)
from fabric_cli.core.fab_types import (
    OneLakeItemType,
    VirtualItemType,
    VirtualWorkspaceItemType,
)
from fabric_cli.utils import fab_util as utils


def exec_command(args: Namespace, context: FabricElement) -> None:
    args.output = utils.process_nargs(args.output)
    args.query = utils.process_nargs(args.query)

    if isinstance(context, Workspace):
        get_workspace.exec(context, args)
    elif isinstance(context, VirtualWorkspaceItem):
        _get_virtual_ws_item(context, args)
    elif isinstance(context, Item):
        get_item.exec(context, args)
    elif isinstance(context, VirtualItem):
        _get_virtual_item(context, args)
    elif isinstance(context, OneLakeItem):
        if context.get_nested_type() == OneLakeItemType.SHORTCUT:
            get_onelake.onelake_shortcut(context, args)
        else:
            get_onelake.onelake_resource(context, args)


# Virtual Workspace Items
def _get_virtual_ws_item(
    virtual_ws_item: VirtualWorkspaceItem, args: Namespace
) -> None:
    match virtual_ws_item.get_item_type():
        case VirtualWorkspaceItemType.CAPACITY:
            get_capacity.exec(virtual_ws_item, args)
        case VirtualWorkspaceItemType.DOMAIN:
            get_domain.exec(virtual_ws_item, args)
        case VirtualWorkspaceItemType.CONNECTION:
            get_connection.exec(virtual_ws_item, args)
        case VirtualWorkspaceItemType.GATEWAY:
            get_gateway.exec(virtual_ws_item, args)
        case _:
            raise FabricCLIError("Not supported")


# Virtual Items
def _get_virtual_item(virtual_item: VirtualItem, args: Namespace) -> None:
    match virtual_item.get_item_type():
        case VirtualItemType.SPARK_POOL:
            get_sparkpool.exec(virtual_item, args)
        case VirtualItemType.MANAGED_PRIVATE_ENDPOINT:
            get_managedprivateendpoint.exec(virtual_item, args)
        case VirtualItemType.EXTERNAL_DATA_SHARE:
            get_externaldatashare.exec(virtual_item, args)
        case _:
            raise FabricCLIError("Not supported")
