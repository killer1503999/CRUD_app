
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from .Resources import *


def gets_secerts(vault_url, secret_name):
    default_credential = ManagedIdentityCredential()
#     default_credential = DefaultAzureCredential(exclude_environment_credential=True, exclude_managed_identity_credential=True,
#                                                 exclude_shared_token_cache_credential=True, exclude_visual_studio_code_credential=True, exclude_cli_credential=False)
    secret_client = SecretClient(
        vault_url=vault_url, credential=default_credential, logging_enable=True)
    secret = secret_client.get_secret(secret_name)
    return secret.value
