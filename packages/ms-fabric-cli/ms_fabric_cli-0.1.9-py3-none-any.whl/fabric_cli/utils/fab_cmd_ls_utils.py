# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_capacity as capacity_api
from fabric_cli.client import fab_api_workspace as workspace_api
from fabric_cli.core.fab_hiearchy import VirtualWorkspaceItem, Workspace


def get_sorted_workspaces(workspaces: list[Workspace]) -> list[dict[str, str]]:
    sorted_workspaces = [
        {"name": ws.get_name(), "id": ws.get_id()} for ws in workspaces
    ]
    return sorted(sorted_workspaces, key=lambda item: item["name"])


def get_capacities_and_workspaces(args: Namespace) -> tuple:
    capacities_response = capacity_api.list_capacities(args)
    capacities = {c["id"]: c for c in json.loads(capacities_response.text)["value"]}

    workspaces_response = workspace_api.list_workspaces(args)
    workspaces = {w["id"]: w for w in json.loads(workspaces_response.text)["value"]}

    return capacities, workspaces


def enrich_workspaces_with_details(
    sorted_workspaces, workspaces_dict, capacities
) -> list[dict[str, str]]:
    for workspace in sorted_workspaces:
        workspace_details = workspaces_dict.get(workspace["id"])
        if workspace_details:
            capacity_id = workspace_details.get("capacityId")
            workspace["capacityId"] = capacity_id
            capacity_details = capacities.get(capacity_id, {})
            workspace["capacityName"] = capacity_details.get("displayName", "N/A")
            workspace["capacityRegion"] = capacity_details.get("region", "Unknown")
    return sorted_workspaces


def update_entry_name_and_type(entry: dict, local_path: str) -> None:
    original_name = entry["name"].split(f"/{local_path}")[-1].lstrip("/")

    if entry.get("isShortcut"):
        entry["name"] = f"{original_name}.Shortcut"
        entry["type"] = "Shortcut"
    # elif "Tables" in entry["name"]:
    #     entry["name"] = original_name
    #     entry["type"] = "TablePath"
    elif entry.get("isDirectory"):
        entry["name"] = original_name
        entry["type"] = "Directory"
    else:
        entry["name"] = original_name
        entry["type"] = "File"


def get_domain_name_by_id(
    domains: list[VirtualWorkspaceItem], domain_id: str | None
) -> str:
    if domain_id == None:
        return ""
    for domain in domains:
        if domain.get_id() == domain_id:
            return domain.get_short_name()
    return ""
