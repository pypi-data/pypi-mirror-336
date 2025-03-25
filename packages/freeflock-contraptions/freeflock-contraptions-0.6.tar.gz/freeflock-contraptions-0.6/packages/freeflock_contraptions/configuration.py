###################
# not thread safe #
###################

import os

from azure.identity import DefaultAzureCredential

_current_configuration = {}
_fetch_variable_function = None


async def collect(variable_name):
    global _current_configuration
    global _fetch_variable_function
    if variable_name not in _current_configuration:
        _current_configuration[variable_name] = await _fetch_variable_function(variable_name)
    return _current_configuration[variable_name]


async def _fetch_variable_from_environment(variable_name):
    return os.environ[variable_name]


async def _fetch_variable_from_azure_key_vault(variable_name):
    global _azure_secret_client
    secret = await _azure_secret_client.get_secret(variable_name)
    value = secret.value
    return value


AZURE_KEY_VAULT_NAME = os.getenv("AZURE_KEY_VAULT_NAME")
if AZURE_KEY_VAULT_NAME is not None:
    from azure.keyvault.secrets.aio import SecretClient

    key_vault_uri = f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net"

    _azure_credential = DefaultAzureCredential()
    _azure_secret_client = SecretClient(vault_url=key_vault_uri, credential=_azure_credential)
    _azure_credential.close()

    _fetch_variable_function = _fetch_variable_from_azure_key_vault
else:
    _fetch_variable_function = _fetch_variable_from_environment
