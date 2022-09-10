from io import BytesIO
import uuid
from pathlib import Path

# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient
from django.conf import settings

from . import models
from azure.storage.blob import BlobServiceClient


ALLOWED_EXTENTIONS = ['.jpg', '.jpeg', '.jpg']


def create_blob_client(file_name):

    #     default_credential = DefaultAzureCredential()

    #     secret_client = SecretClient(
    #         vault_url=settings.AZURE_VAULT_ACCOUNT, credential=default_credential
    #     )

    #     storage_credentials = secret_client.get_secret(
    #         name=settings.AZURE_STORAGE_KEY_NAME)
    #     account_url = "https://assessmentstgacc.blob.core.windows.net/?sv=2021-06-08&ss=bfqt&srt=o&sp=rwdlacupiytfx&se=2022-11-05T03:54:23Z&st=2022-09-06T19:54:23Z&spr=https&sig=cV6yqihn5pkNcRdM0s4inOyQOTywVxYMh7davBmeH58%3D"

    #     print(settings.AZURE_STORAGE_ACCOUNT)
    #     print(settings.AZURE_APP_BLOB_NAME)
    #     print(file_name)
    #     print(BlobClient(
    #         account_url=settings.AZURE_STORAGE_ACCOUNT,
    #         container_name=settings.AZURE_APP_BLOB_NAME,
    #         blob_name=file_name,
    #         credential=None,
    #     ))

    return BlobClient(
        account_url=settings.AZURE_STORAGE_ACCOUNT,
        container_name=settings.AZURE_APP_BLOB_NAME,
        blob_name=file_name,
        credential=None,
    )
#     BlobClient(account_url: str, container_name: str, blob_name: str, snapshot: Optional[Union[str, Dict[str, Any]]] = None, credential: Optional[Any] = None, **kwargs: Any)


def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENTIONS


def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content


def upload_file_to_blob(file):
    #     print(file.name)

    if not check_file_ext(file.name):
        return

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    blob_client = create_blob_client(file_name=file_name)
    blob_client.upload_blob(data=file_io)

#     blob_client.set_blob_metadata(container_name=settings.AZURE_APP_BLOB_NAME,
#                                   blob_name=file_name,
#                                   x_ms_meta_name_values={"factoryId": FactoryId})
    file_object = file_name
    print("file uploaded to", file_object)
#     blob_service_client = BlobServiceClient(
    #   account_url=settings.AZURE_STORAGE_ACCOUNT, credential=None)
#     blob_service_client.set_blob_metadata(container_name=settings.AZURE_APP_BLOB_NAME,
#                                           blob_name=file_name,
#                                           x_ms_meta_name_values={"factoryId": 1})

    return file_object


def delete_blob_client(file_name):
    blob_client = create_blob_client(file_name)
    print(settings.AZURE_BLOB_PATH+file_name)
    blob_client.delete_blob()
    return True
