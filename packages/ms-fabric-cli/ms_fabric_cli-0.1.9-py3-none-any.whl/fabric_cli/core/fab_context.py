# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_hiearchy import FabricElement, Tenant
from fabric_cli.core.fab_types import FabricElementType
from fabric_cli.utils import fab_ui as utils_ui


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Context:
    def __init__(self):
        # Initialize the context
        self.context: FabricElement = None
        self.command: str = None

    def load_context(self) -> None:
        self.set_context(FabAuth().get_tenant())

    def reset_context(self) -> None:
        self.context = self.get_context().get_tenant()

    def print_context(self) -> None:
        utils_ui.print_grey(str(self.get_context()))

    def get_context_type(self) -> FabricElementType:
        return self.get_context().get_type()

    def get_context(self) -> FabricElement:
        if self.context is None:
            self.load_context()
        return self.context

    def set_context(self, context: FabricElement) -> None:
        self.context = context
    
    def set_command(self, command: str) -> None:
        self.command = command
    
    def get_command(self) -> str:
        return self.command

    # Tenant

    def get_tenant(self) -> Tenant:
        return self.get_context().get_tenant()

    def get_tenant_id(self) -> str:
        return self.get_tenant().get_id()
