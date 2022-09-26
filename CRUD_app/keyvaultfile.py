
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from .Resources import *


def gets_secerts(vault_url, secret_name):
    default_credential = ManagedIdentityCredential()
#     default_credential = DefaultAzureCredential(exclude_environment_credential=True, exclude_managed_identity_credential=True,
#                                                 exclude_shared_token_cache_credential=True, exclude_visual_studio_code_credential=True, exclude_cli_credential=False)
    secret_client = SecretClient(
        vault_url=vault_url, credential=default_credential, logging_enable=True)

    # os.environ["Data_AzureConnection"]

    secret = secret_client.get_secret(secret_name)

#     keys = secret_client.list_properties_of_secrets()

#     for key in keys:
#         # the list doesn't include values or versions of the keys
#         print(key.name)
#         secret = secret_client.get_secret(key.name)
#         print(secret.value)

    return secret.value


print(gets_secerts(vault_url, "BlobSasUrl"))
