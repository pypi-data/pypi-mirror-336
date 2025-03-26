# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace
from typing import Any

import jwt

from fabric_cli.core import fab_constant, fab_logger, fab_state_config
from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_context import Context
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.utils import fab_mem_store as utils_mem_store
from fabric_cli.utils import fab_ui as utils_ui


def init(args: Namespace) -> Any:
    auth_options = [
        "Interactive with a web browser",
        "Service principal authentication with secret",
        "Service principal authentication with certificate",
        "Managed identity authentication",
    ]

    utils_mem_store.clear_caches()

    if args.identity:
        FabAuth().set_access_mode("managed_identity")
        FabAuth().set_managed_identity(args.username)
        FabAuth().get_access_token(scope=fab_constant.SCOPE_FABRIC_DEFAULT)
        FabAuth().get_access_token(scope=fab_constant.SCOPE_ONELAKE_DEFAULT)
        FabAuth().get_access_token(scope=fab_constant.SCOPE_AZURE_DEFAULT)
        Context().set_context(FabAuth().get_tenant())
        fab_state_config.init_defaults()

    elif any([args.username, args.password]):
        if not (
            all([args.username, args.tenant]) and any([args.password, args.certificate])
        ):
            raise FabricCLIError(
                "-u/--username and -t/--tenant all must be provided. -p/--password or --certificate must be provided.",
                fab_constant.ERROR_INVALID_INPUT,
            )
        else:
            FabAuth().set_access_mode("service_principal")
            FabAuth().set_tenant(args.tenant)
            if args.certificate:
                FabAuth().set_spn(
                    args.username, cert_path=args.certificate, password=args.password
                )
            elif args.password:
                FabAuth().set_spn(args.username, password=args.password)
            FabAuth().get_access_token(scope=fab_constant.SCOPE_FABRIC_DEFAULT)
            FabAuth().get_access_token(scope=fab_constant.SCOPE_ONELAKE_DEFAULT)
            FabAuth().get_access_token(scope=fab_constant.SCOPE_AZURE_DEFAULT)
            Context().set_context(FabAuth().get_tenant())
            fab_state_config.init_defaults()
    else:
        selected_auth = utils_ui.prompt_select_item(
            "How would you like to authenticate Fabric CLI?", auth_options
        )
        # When user cancels the prompt, selected_auth will be None
        if selected_auth is None:
            return False

        try:
            if selected_auth == "Interactive with a web browser":
                if getattr(args, "tenant", None) is not None:
                    FabAuth().set_tenant(args.tenant)
                FabAuth().set_access_mode("user")
                FabAuth().get_access_token(scope=fab_constant.SCOPE_FABRIC_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_ONELAKE_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_AZURE_DEFAULT)
                Context().set_context(FabAuth().get_tenant())
                fab_state_config.init_defaults()
            elif selected_auth.startswith("Service principal authentication"):
                fab_logger.log_warning(
                    "Ensure tenant setting is enabled for Service Principal auth"
                )

                tenant_id = utils_ui.prompt_ask("Enter tenant ID:")
                if not tenant_id:
                    return

                client_id = utils_ui.prompt_ask("Enter client ID:")
                if not client_id:
                    return

                if selected_auth == "Service principal authentication with certificate":
                    cert_path = utils_ui.prompt_ask(
                        "Enter certificate path (PEM, PKCS12 formats):"
                    )
                    if not cert_path:
                        return
                    cert_password = utils_ui.prompt_password(
                        "Enter certificate password (optional):"
                    )
                elif selected_auth == "Service principal authentication with secret":
                    cert_path = None
                    client_secret = utils_ui.prompt_password("Enter client secret:")
                    if not client_secret:
                        return

                FabAuth().set_access_mode("service_principal")
                FabAuth().set_tenant(tenant_id)
                if cert_path:
                    FabAuth().set_spn(
                        client_id, cert_path=cert_path, password=cert_password
                    )
                elif client_secret:
                    FabAuth().set_spn(client_id, password=client_secret)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_FABRIC_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_ONELAKE_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_AZURE_DEFAULT)
                Context().set_context(FabAuth().get_tenant())
                fab_state_config.init_defaults()
            elif selected_auth == "Managed identity authentication":
                fab_logger.log_warning(
                    "Ensure tenant setting is enabled for Service Principal auth"
                )
                client_id = utils_ui.prompt_ask(
                    "Enter client ID (only for User Assigned):"
                )
                FabAuth().set_access_mode("managed_identity")
                FabAuth().set_managed_identity(client_id)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_FABRIC_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_ONELAKE_DEFAULT)
                FabAuth().get_access_token(scope=fab_constant.SCOPE_AZURE_DEFAULT)
                Context().set_context(FabAuth().get_tenant())
                fab_state_config.init_defaults()

        except KeyboardInterrupt:
            # User cancelled the authentication process
            return False
        return True


def logout(args: Namespace) -> None:
    FabAuth().logout()

    # Clear cache and context
    utils_mem_store.clear_caches()
    Context().reset_context()

    utils_ui.print_done("Logged out of Fabric account")


def status(args: Namespace) -> None:
    auth = FabAuth()
    tenant_id = auth.get_tenant_id()

    def __get_token_info(scope):
        try:
            token = auth.get_access_token(scope, interactive_renew=False)
        except FabricCLIError as e:
            if e.status_code == fab_constant.ERROR_UNAUTHORIZED:
                return {}
            else:
                raise e
        if isinstance(token, str):
            token = token.encode()  # Ensure bytes type
        return _get_token_info_from_bearer_token(token) if token else {}

    token_info = __get_token_info(fab_constant.SCOPE_FABRIC_DEFAULT)

    upn = token_info.get("upn") or "N/A"
    oid = token_info.get("oid") or "N/A"

    def __mask_token(scope):
        try:
            token = auth.get_access_token(scope, interactive_renew=False)
        except FabricCLIError as e:
            if e.status_code == fab_constant.ERROR_UNAUTHORIZED:
                return "N/A"
            else:
                raise e
        if isinstance(token, str):
            token = token.encode()  # Ensure bytes type
        return (
            token[:4].decode() + "************************************"
            if token
            else "N/A"
        )

    fabric_secret = __mask_token(fab_constant.SCOPE_FABRIC_DEFAULT)
    storage_secret = __mask_token(fab_constant.SCOPE_ONELAKE_DEFAULT)
    azure_secret = __mask_token(fab_constant.SCOPE_AZURE_DEFAULT)

    # Check login status
    login_status = (
        "✓ Logged in to app.fabric.microsoft.com"
        if fabric_secret != "N/A"
        else "✗ Not logged in to app.fabric.microsoft.com"
    )

    utils_ui.print_grey(
        f"""{login_status}
  - Account: {upn} ({oid})
  - Tenant ID: {tenant_id}
  - Token (fabric/powerbi): {fabric_secret}
  - Token (storage): {storage_secret}
  - Token (azure): {azure_secret}"""
    )


# Utils
def _get_token_info_from_bearer_token(bearer_token: str) -> dict[str, str]:
    payload = jwt.decode(bearer_token, options={"verify_signature": False})

    # https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
    upn = payload.get("upn")
    oid = payload.get("oid")

    return {"upn": upn, "oid": oid}
