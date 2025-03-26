# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import os
import re
from typing import Any, List

from fabric_cli.core import fab_commands as cmd
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_commands import Command
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_types import (
    FabricElementType,
    FabricJobType,
    ItemFoldersMap,
    ItemType,
    ITJobMap,
    ITMutablePropMap,
    OneLakeItemType,
    VICMap,
    VirtualItemContainerType,
    VirtualItemType,
    VirtualWorkspaceItemType,
    VirtualWorkspaceType,
    VWIMap,
    WorkspaceType,
)

##########################################################################################################
# Fabric Element Hiearchy Classes                                                                        #
##########################################################################################################
#                                                                                       (FabricElement)  #
##########################################################################################################
#                   Tenant                                             LocalPath      |                  #
#           __________|__________ _ _ _ _ _ _ _ _ _ _ _                               |                  #
#          |                    |                      |                              |                  #
#  Virtual Workspace        Workspace ----->  Virtual Item Container                  | (_BaseWorkspace) #
#          |                    | _ _ _ _ _ _ _ _ _ _ _|                              |                  #
#          |                    |                      |                              |                  #
#  Virtual Ws Item            Item               Virtual Item                         | (_BaseItem)      #
#                               |                                                     |                  #
#                            OneLake                                                  | (_BaseSubItem)   #
#                                                                                     |                  #
##########################################################################################################


##########################################################################################################
# Fabric Element Classes                                                                                 #
##########################################################################################################


class FabricElement:
    def __init__(self, name, id, element_type: FabricElementType, parent=None):
        self._name = name
        self._id = id
        self._type = element_type
        self._parent = parent

    def __str__(self) -> str:
        return f"[{self._type}] ({self._name}, {self._id})"

    def __eq__(self, value) -> bool:
        if not isinstance(value, FabricElement):
            return False
        _eq_id = self.get_id() == value.get_id()
        _eq_name = self.get_name() == value.get_name()
        _eq_type = self.get_type() == value.get_type()
        _eq_parent = self.get_parent() == value.get_parent()
        return _eq_id and _eq_name and _eq_type and _eq_parent

    def get_id(self) -> str:
        return self._id

    def get_short_name(self) -> str:
        return self._name

    def get_full_name(self) -> str:
        return f"{self._name}.{self._type}"

    def get_name(self) -> str:
        return self.get_full_name()

    def get_type(self) -> FabricElementType:
        return self._type

    def get_parent(self) -> Any:
        return self._parent

    def get_path(self) -> str:
        if self.get_parent() is None:
            return "/"

        name_scaped = self.get_name().replace("/", "\/")
        return f"{self.get_parent().get_path().rstrip('/')}/{name_scaped}"

    def get_path_id(self) -> str:
        if self.get_parent() is None:
            return "/"
        return f"{self.get_parent().get_path_id().rstrip('/')}/{self.get_id()}"

    def get_tenant(self) -> Any:
        if self.get_type() == FabricElementType.TENANT:
            return self
        else:
            return self.get_parent().get_tenant()

    def check_command_support(self, commmand: Command) -> bool:
        """Check if the element type supports the command."""
        is_supported = self.get_type() in cmd.get_supported_elements(commmand)
        if not is_supported:
            raise FabricCLIError(
                # f"{self.get_type()} is not supported for command '{commmand.value}'",
                f"not supported for command '{commmand.value}'",
                fab_constant.WARNING_UNSUPPORTED_COMMAND,
            )
        return True

    def is_ascendent(self, element) -> bool:
        if not isinstance(element, FabricElement):
            return False
        if self == element:
            return True
        if self.get_parent() is None:
            return False
        return self.get_parent().is_ascendent(element)


class Tenant(FabricElement):
    def __init__(self, name, id):
        super().__init__(name, id, FabricElementType.TENANT)


class LocalPath(FabricElement):
    def __init__(self, name, id, path):
        super().__init__(name, id, FabricElementType.LOCAL_PATH)
        self._path = path

    def get_path(self) -> str:
        return self._path

    def is_file(self) -> bool:
        return os.path.isfile(self._path)

    def is_directory(self) -> bool:
        return os.path.isdir(self._path)

    def get_name(self) -> str:
        return os.path.basename(self._path)


class _BaseWorkspace(FabricElement):

    def __init__(self, name, id, element_type, parent: Tenant):
        super().__init__(name, id, element_type, parent)

    def get_tenant_id(self) -> str:
        return self.get_parent().get_id()

    def get_tenant_name(self) -> str:
        return self.get_parent().get_name()

    def get_workspace_id(self) -> str:
        return self.get_id()

    def get_workspace_name(self) -> str:
        return self.get_name()


class Workspace(_BaseWorkspace):
    @staticmethod
    def validate_name(name) -> tuple[str, WorkspaceType]:
        # Workspace name should be in the format <name>.Workspace or <name>.Personal
        pattern = r"^(.+)\.(\w+)$"
        match = re.match(pattern, name, re.IGNORECASE)
        if match:
            # Capitalize the first letter of the workspace type
            _name = match.group(1)
            _type = WorkspaceType.from_string(match.group(2))
            return (_name, _type)
        else:
            raise FabricCLIError(
                f"Invalid workspace name '{name}'",
                fab_constant.WARNING_INVALID_WORKSPACE_NAME,
            )

    def __init__(self, name, id, parent: Tenant, type: str):
        super().__init__(name, id, FabricElementType.WORKSPACE, parent)
        # Old workspaces do not comply with the new naming convention
        if id is None:
            (_, _type) = Workspace.validate_name(f"{name}.{type}")
        else:
            _type = WorkspaceType.from_string(str(type))
        self.ws_type = _type

    def __eq__(self, value) -> bool:
        if not isinstance(value, Workspace):
            return False
        _eq_ws_type = self.get_ws_type() == value.get_ws_type()
        return super().__eq__(value) and _eq_ws_type

    def get_full_name(self) -> str:
        return f"{super().get_short_name()}.{self.get_ws_type()}"

    def get_ws_type(self) -> WorkspaceType:
        return self.ws_type


class VirtualWorkspace(_BaseWorkspace):
    @staticmethod
    def validate_name(name) -> tuple[str, VirtualWorkspaceType]:
        """Normalize the virtual workspace name."""
        try:
            vws_type = VirtualWorkspaceType.from_string(name)
        except FabricCLIError:
            raise FabricCLIError(
                f"Invalid type '{name}'",
                fab_constant.WARNING_INVALID_WORKSPACE_TYPE,
            )
        return (str(vws_type), vws_type)

    def __init__(self, name, id, parent: Tenant):
        super().__init__(name, id, FabricElementType.VIRTUAL_WORKSPACE, parent)
        (_, _type) = VirtualWorkspace.validate_name(f"{name}")
        self.vws_type = _type
        self.item_type = VWIMap[_type]

    def __eq__(self, value) -> bool:
        if not isinstance(value, VirtualWorkspace):
            return False
        _eq_vws_type = self.get_vws_type() == value.get_vws_type()
        _eq_item_type = self.get_item_type() == value.get_item_type()
        return super().__eq__(value) and _eq_vws_type and _eq_item_type

    def get_full_name(self) -> str:
        return super().get_short_name()

    def get_vws_type(self) -> VirtualWorkspaceType:
        return self.vws_type

    def get_item_type(self) -> VirtualWorkspaceItemType:
        return self.item_type


class VirtualItemContainer(FabricElement):
    @staticmethod
    def validate_name(name) -> tuple[str, VirtualItemContainerType]:
        """Normalize the virtual item container name."""
        try:
            vic_type = VirtualItemContainerType.from_string(name)
        except FabricCLIError:
            raise FabricCLIError(
                f"Invalid type '{name}'",
                fab_constant.WARNING_INVALID_ITEM_TYPE,
            )
        return (str(vic_type), vic_type)

    def __init__(self, name, id, parent: Workspace):
        super().__init__(name, id, FabricElementType.VIRTUAL_ITEM_CONTAINER, parent)
        (_, _type) = VirtualItemContainer.validate_name(f"{name}")
        self.vic_type = _type
        self.item_type = VICMap[_type]

    def __eq__(self, value) -> bool:
        if not isinstance(value, VirtualItemContainer):
            return False
        _eq_vit_type = self.get_vic_type() == value.get_vic_type()
        _eq_item_type = self.get_item_type() == value.get_item_type()
        return super().__eq__(value) and _eq_vit_type and _eq_item_type

    def get_tenant_id(self) -> str:
        return self.get_parent().get_tenant_id()

    def get_tenant_name(self) -> str:
        return self.get_parent().get_tenant_name()

    def get_workspace_id(self) -> str:
        return self.get_parent().get_id()

    def get_workspace_name(self) -> str:
        return self.get_parent().get_name()

    def get_full_name(self) -> str:
        return super().get_short_name()

    def get_vic_type(self) -> VirtualItemContainerType:
        return self.vic_type

    def get_item_type(self) -> VirtualItemType:
        return self.item_type

    def get_path_id(self) -> str:
        return self.get_parent().get_path_id()


class _BaseItem(FabricElement):
    @staticmethod
    def _validate_name(name, sub_class_type) -> tuple[str, Any]:
        """Normalize the item name."""
        # Item name should be in the format <name>.<type>
        # Item name can only contain alphanumeric characters, spaces, underscores, and hyphens
        # Item name should not end with a space
        pattern = r"^(.*)\.([a-zA-Z0-9_-]+)$"
        match = re.match(pattern, name, re.IGNORECASE)
        if match:
            item_type = sub_class_type.from_string(match.group(2))
            strict_name_pattern = r"[^a-zA-Z0-9_]"
            unsupported_types = {
                ItemType.LAKEHOUSE,
                ItemType.ML_EXPERIMENT,
                ItemType.ML_MODEL,
                ItemType.EVENTSTREAM,
            }
            if (
                re.search(strict_name_pattern, match.group(1))
                and item_type in unsupported_types
            ):
                raise FabricCLIError(
                    f"{item_type} name '{match.group(1)}' contains unsupported special characters",
                    fab_constant.WARNING_INVALID_SPECIAL_CHARACTERS,
                )
            return (match.group(1), item_type)
        else:
            raise FabricCLIError(
                f"Invalid item name '{name}'",
                fab_constant.WARNING_INVALID_ITEM_NAME,
            )

    def __init__(self, name, id, element_type, parent, item_type=None):
        super().__init__(name, id, element_type, parent)
        self.item_type = item_type

    def __eq__(self, value) -> bool:
        if not isinstance(value, _BaseItem):
            return False
        _eq_item_type = self.get_item_type() == value.get_item_type()
        return super().__eq__(value) and _eq_item_type

    def get_full_name(self) -> str:
        return f"{super().get_short_name()}.{self.get_item_type()}"

    def get_tenant_id(self) -> str:
        return self.get_parent().get_tenant_id()

    def get_tenant_name(self) -> str:
        return self.get_parent().get_tenant_name()

    def get_workspace(self) -> _BaseWorkspace:
        return self.get_parent()

    def get_workspace_id(self) -> str:
        return self.get_workspace().get_id()

    def get_workspace_name(self) -> str:
        return self.get_workspace().get_name()

    def get_item_type(self) -> Any:
        return self.item_type

    def check_command_support(self, commmand: Command) -> bool:
        """Check if the element type supports the command."""
        is_unsupported = self.get_item_type() in cmd.get_unsupported_items(commmand)
        is_supported = self.get_item_type() in cmd.get_supported_items(commmand)
        if is_unsupported:
            raise FabricCLIError(
                # f"{self.get_item_type()} is not supported for command '{commmand.value}'",
                f"not supported for command '{commmand.value}'",
                fab_constant.WARNING_UNSUPPORTED_COMMAND,
            )
        if is_supported:
            return True
        try:
            super().check_command_support(commmand)
        except FabricCLIError:
            raise FabricCLIError(
                # f"{self.get_item_type()} is not supported for command '{commmand.value}'",
                f"not supported for command '{commmand.value}'",
                fab_constant.WARNING_UNSUPPORTED_COMMAND,
            )
        return True


class Item(_BaseItem):
    @staticmethod
    def validate_name(name) -> tuple[str, ItemType]:
        return _BaseItem._validate_name(name, ItemType)

    def __init__(self, name, id, parent: Workspace, item_type: str):
        if id is None:
            (_, _type) = Item.validate_name(f"{name}.{item_type}")
        else:
            _type = ItemType.from_string(
                str(item_type)
            )  # TODO: Do the same for the rest of Items that inherit from the _BaseItem class

        super().__init__(name, id, FabricElementType.ITEM, parent, _type)

    def get_item_type(self) -> ItemType:
        return super().get_item_type()

    def get_job_type(self) -> FabricJobType:
        return ITJobMap[self.get_item_type()]

    def get_mutable_properties(self) -> List[str]:
        item_type = self.get_item_type()
        properties = []

        if item_type in ITMutablePropMap:
            properties = [list(prop.keys())[0]
                          for prop in ITMutablePropMap[item_type]]
        return properties + ["displayName", "description"]

    def get_property_value(self, key: str) -> str:
        item_type = self.get_item_type()
        properties = [
            {"displayName": "displayName"},
            {"description": "description"},
        ]

        if item_type in ITMutablePropMap:
            properties = ITMutablePropMap[item_type] + properties

        for prop in properties:
            if key in prop:
                return prop[key]

        raise FabricCLIError(
            f"Key '{key}' not found in item mutable properties")

    def get_parent(self) -> Workspace:
        return super().get_parent()

    def get_workspace(self) -> Workspace:
        return super().get_parent()

    def get_payload(self, definition, input_format=None) -> dict:
        match self.get_item_type():

            case ItemType.SPARK_JOB_DEFINITION:
                return {
                    "type": str(self.get_item_type()),
                    "description": "Imported from fab",
                    "displayName": self.get_short_name(),
                    "definition": {
                        "format": "SparkJobDefinitionV1",
                        "parts": definition["parts"],
                    },
                }
            case ItemType.NOTEBOOK:
                return {
                    "type": str(self.get_item_type()),
                    "description": "Imported from fab",
                    "displayName": self.get_short_name(),
                    "definition": {
                        **(
                            {"parts": definition["parts"]}
                            if input_format == ".py"
                            else {"format": "ipynb", "parts": definition["parts"]}
                        )
                    },
                }
            case (
                ItemType.REPORT
                | ItemType.SEMANTIC_MODEL
                | ItemType.KQL_DASHBOARD
                | ItemType.DATA_PIPELINE
                | ItemType.KQL_QUERYSET
                | ItemType.EVENTHOUSE
                | ItemType.KQL_DATABASE
                | ItemType.MIRRORED_DATABASE
                | ItemType.REFLEX
                | ItemType.EVENTSTREAM
                | ItemType.MOUNTED_DATA_FACTORY
            ):
                return {
                    "type": str(self.get_item_type()),
                    "description": "Imported from fab",
                    "displayName": self.get_short_name(),
                    "definition": definition,
                }
            case _:
                raise FabricCLIError(
                    f"{self.get_item_type()} doesn't support definition payload",
                    fab_constant.WARNING_UNSUPPORTED_COMMAND,
                )

    def get_folders(self) -> List[str]:
        return ItemFoldersMap.get(self.get_item_type(), [])


class VirtualItem(_BaseItem):
    @staticmethod
    def validate_name(name) -> tuple[str, VirtualItemType]:
        return _BaseItem._validate_name(name, VirtualItemType)

    def __init__(self, name, id, parent: VirtualItemContainer, item_type: str):
        (_, _type) = VirtualItem.validate_name(f"{name}.{item_type}")
        super().__init__(name, id, FabricElementType.VIRTUAL_ITEM, parent, _type)

    def get_item_type(self) -> VirtualItemType:
        return super().get_item_type()

    def get_parent(self) -> VirtualItemContainer:
        return super().get_parent()

    def get_workspace(self) -> Workspace:
        return self.get_parent().get_parent()


class ExternalDataShareVirtualItem(VirtualItem):
    def __init__(
        self,
        name,
        id,
        parent: VirtualItemContainer,
        item_type: str,
        status: str,
        item_id: str,
    ):
        super().__init__(name, id, parent, item_type)
        self.status = status
        self.item_id = item_id

    def get_status(self) -> str:
        return self.status

    def get_item_id(self) -> str:
        return self.item_id


class VirtualWorkspaceItem(_BaseItem):
    @staticmethod
    def validate_name(name) -> tuple[str, VirtualWorkspaceItemType]:
        return _BaseItem._validate_name(name, VirtualWorkspaceItemType)

    def __init__(self, name, id, parent: VirtualWorkspace, item_type: str):
        (_, _type) = VirtualWorkspaceItem.validate_name(f"{name}.{item_type}")
        super().__init__(
            name, id, FabricElementType.VIRTUAL_WORKSPACE_ITEM, parent, _type
        )

    def get_item_type(self) -> VirtualWorkspaceItemType:
        return super().get_item_type()

    def get_parent(self) -> VirtualWorkspace:
        return super().get_parent()


class _BaseSubItem(FabricElement):
    def __init__(
        self,
        name,
        id,
        element_type: FabricElementType,
        parent: FabricElement,
        nested_type=None,
    ):
        assert isinstance(parent, _BaseItem) or isinstance(
            parent, _BaseSubItem)
        super().__init__(name, id, element_type, parent)
        self.nested_type = nested_type

    def __eq__(self, value):
        if not isinstance(value, _BaseSubItem):
            return False
        _eq_nested_type = self.get_nested_type() == value.get_nested_type()
        return super().__eq__(value) and _eq_nested_type

    def get_tenant_id(self) -> str:
        return self.get_parent().get_tenant_id()

    def get_tenant_name(self) -> str:
        return self.get_parent().get_tenant_name()

    def get_workspace_id(self) -> str:
        return self.get_parent().get_workspace_id()

    def get_workspace_name(self) -> str:
        return self.get_parent().get_workspace_name()

    def get_item(self) -> Item:
        if isinstance(self.get_parent(), Item):
            return self.get_parent()
        else:
            return self.get_parent().get_item()

    def get_item_id(self) -> str:
        if isinstance(self.get_parent(), Item):
            return self.get_parent().get_id()
        else:
            return self.get_parent().get_item_id()

    def get_item_name(self) -> str:
        if isinstance(self.get_parent(), Item):
            return self.get_parent().get_name()
        else:
            return self.get_parent().get_item_name()

    def get_item_type(self) -> ItemType:
        return self.get_parent().get_item_type()

    def get_nested_type(self) -> Any:
        return self.nested_type


class OneLakeItem(_BaseSubItem):
    def __init__(self, name, id, parent: FabricElement, nested_type: OneLakeItemType):
        assert isinstance(parent, Item) or isinstance(parent, OneLakeItem)
        super().__init__(name, id, FabricElementType.ONELAKE, parent, nested_type)
        if isinstance(parent, Item):
            self.root_folder = name

    def __eq__(self, value):
        if not isinstance(value, OneLakeItem):
            return False
        _eq_local_path = self.get_path().rstrip("/") == value.get_path().rstrip("/")
        return super().__eq__(value) and _eq_local_path

    def get_parent_item(self) -> Item:
        if isinstance(self.get_parent(), Item):
            return self.get_parent()
        elif isinstance(self.get_parent(), OneLakeItem):
            return self.get_parent().get_parent_item()
        else:
            raise FabricCLIError(
                f"Invalid parent type: {type(self.get_parent())}")

    def get_full_name(self):
        if self.nested_type == OneLakeItemType.SHORTCUT:
            return f"{self.get_short_name()}.Shortcut"
        else:
            return self.get_short_name()

    def get_local_path(self):
        if isinstance(self.get_parent(), Item):
            return f"{self.get_short_name()}"
        else:
            return f"{self.get_parent().get_local_path()}/{self.get_short_name()}"

    def get_path(self):
        return f"{self.get_parent().get_path()}/{self.get_full_name()}"

    def get_path_id(self):
        return f"{self.get_parent().get_path_id()}/{self.get_short_name()}"

    def get_root_folder(self):
        if isinstance(self.get_parent(), Item):
            return self.root_folder
        else:
            return self.get_parent().get_root_folder()

    def is_shortcut_path(self):
        if isinstance(self.get_parent(), Item):
            return self.nested_type == OneLakeItemType.SHORTCUT
        elif isinstance(self.get_parent(), OneLakeItem):
            return self.nested_type == OneLakeItemType.SHORTCUT or self.get_parent().is_shortcut_path()
