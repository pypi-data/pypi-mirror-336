###################
# not thread safe #
###################

import os

_current_configuration = {}
_fetch_variable_function = None


def collect_from_config(variable_name):
    global _current_configuration
    global _fetch_variable_function
    if variable_name not in _current_configuration:
        _current_configuration[variable_name] = _fetch_variable_function(variable_name)
    return _current_configuration[variable_name]


def _fetch_variable_from_environment(variable_name):
    return os.environ[variable_name]


def _fetch_variable_from_azure_key_vault(variable_name):
    global _azure_secret_client
    formatted_variable_name = variable_name.lower().replace("_", "-")
    secret = _azure_secret_client.get_secret(formatted_variable_name)
    value = secret.value
    return value


AZURE_KEY_VAULT_NAME = os.getenv("AZURE_KEY_VAULT_NAME")
if AZURE_KEY_VAULT_NAME is not None:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    key_vault_uri = f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net"

    _azure_credential = DefaultAzureCredential()
    _azure_secret_client = SecretClient(vault_url=key_vault_uri, credential=_azure_credential)
    _azure_credential.close()

    _fetch_variable_function = _fetch_variable_from_azure_key_vault
else:
    _fetch_variable_function = _fetch_variable_from_environment
