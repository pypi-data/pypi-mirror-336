# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import argparse
from typing import Optional

from fabric_cli.core import fab_logger
from fabric_cli.utils import fab_ui as utils_ui


def invalid_choice(self, message: Optional[str] = None) -> None:
    try:
        # Get the current subparser command from the context
        command_name = self.prog.split()[-1]

        # Retrieve all available commands from the subparsers
        available_commands = set()
        seen_subparsers = set()

        for action in self._subparsers._group_actions:
            if isinstance(action, argparse._SubParsersAction):
                for command, subparser in action.choices.items():
                    if subparser not in seen_subparsers:
                        if command not in {"clear", "version", "cls"}:
                            available_commands.add(command)
                            seen_subparsers.add(
                                subparser
                            )  # Mark this subparser as seen

        # Format the list of available commands
        command_list = "\n  ".join(sorted(available_commands))

        self.prog = self.prog.replace("fab ", "")
        usage_format = (
            f"{self.prog} <subcommand> [flags]"
            if command_name != "fab"
            else f"<command> <subcommand> [flags]"
        )

        fab_logger.log_warning(f'unknown command for "{command_name}"\n')
        custom_message = (
            f"Usage:  {usage_format}\n\n" f"Available commands:\n  {command_list}\n"
        )
        utils_ui.print(custom_message)

    except Exception as e:
        if message:
            fab_logger.log_warning(message)


def unrecognized_arguments(message: str) -> None:
    _, unrecognized_args = message.split(":", 1)
    fab_logger.log_warning(f"unknown shorthand flag: {unrecognized_args}")


def missing_required_arguments(message: str) -> None:
    _, required_args = message.split(":", 1)
    fab_logger.log_warning(f"missing arg(s): {required_args}")


def invalid_for_command_line_mode() -> None:
    fab_logger.log_warning("invalid command usage")
    custom_message = (
        f"Usage:  fab -c '<command> <subcommand> [flags]' or enter interactive mode\n"
    )
    utils_ui.print(custom_message)


def get_usage_prog(parser: argparse.ArgumentParser) -> str:
    # Removes 'fab' from %(prog)s
    # Start with the command (like "acl ls" or "acl dir")
    command_part = " ".join(parser.prog.split()[1:])

    # Collect positional arguments in `<...>`
    pos_args = [f"<{arg.dest}>" for arg in parser._get_positional_actions()]

    # Collect optional (flag) arguments in `[...]`
    opt_args = [
        f"[{arg.option_strings[0]}]"
        for arg in parser._get_optional_actions()
        if arg.option_strings
    ]

    # Combine parts for the final usage string
    return f"{command_part} {' '.join(pos_args)} {' '.join(opt_args)}"
