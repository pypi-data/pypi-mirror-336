# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import webbrowser
from argparse import Namespace

from fabric_cli.core import fab_constant, fab_logger, fab_state_config
from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_hiearchy import FabricElement, Item, Workspace
from fabric_cli.core.fab_types import uri_mapping
from fabric_cli.utils import fab_ui as utils_ui

COMMAND = "open"


def exec_command(args: Namespace, context: FabricElement) -> None:
    if isinstance(context, Workspace):
        _open_workspace(context)
    elif isinstance(context, Item):
        _open_item(context)


# Workspaces
def _open_workspace(workspace: Workspace) -> None:
    workspace_id = workspace.get_id()
    experience = _get_ux_experience()

    if workspace_id:
        url = f"{fab_constant.WEB_URI}/{workspace_id}/list?experience={experience}"
        _open_in_browser(url, workspace.get_name())


# Items
def _open_item(item: Item) -> None:
    workspace_id = item.get_workspace_id()
    item_id = item.get_id()
    experience = _get_ux_experience()

    if workspace_id and item_id:
        url = f"{fab_constant.WEB_URI}/{workspace_id}/{uri_mapping.get(item.get_item_type(), '')}/{item_id}/?experience={experience}"
        _open_in_browser(url, item.get_name())


# Utils
def _open_in_browser(url: str, name: str) -> None:
    utils_ui.print_grey(f"Opening '{name}' in the web browser...")
    utils_ui.print_done(f"{url}")

    if FabAuth()._get_auth_property(fab_constant.FAB_AUTH_MODE) != "user":
        fab_logger.log_error("Only supported with user authentication", COMMAND)
        return
    else:
        upn = FabAuth().get_token_claim(fab_constant.SCOPE_FABRIC_DEFAULT, "upn")
        if upn:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}upn={upn}"

        webbrowser.open_new(url)


def _get_ux_experience() -> str:
    if (
        fab_state_config.get_config(fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE)
        == "powerbi"
    ):
        return fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE_POWERBI
    else:
        return fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE_FABRIC
