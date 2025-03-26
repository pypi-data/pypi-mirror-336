# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace) -> None:
    try:
        with open(args.input, "r") as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        raise FabricCLIError(
            fab_constant.WARNING_INVALID_JSON_FORMAT, fab_constant.ERROR_INVALID_JSON
        )
    except Exception as e:
        raise FabricCLIError(
            "No such file or directory", fab_constant.ERROR_INVALID_PATH
        )

    try:
        columns = ["name", "id"]
        utils_ui.print_entries_unix_style(data["labels"], columns, header=True)
    except Exception as e:
        raise FabricCLIError(
            "Invalid entries format in labels definition file",
            fab_constant.ERROR_INVALID_ENTRIES_FORMAT,
        )
