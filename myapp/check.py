# Create your views here.

from azure.storage.blob import BlobClient


def delete_blob_client(file_name):
    blob_client = BlobClient(
        account_url="https://assessmentstgacc.blob.core.windows.net/?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2022-10-01T16:50:11Z&st=2022-09-07T08:50:11Z&spr=https&sig=9jUrQufsLJGf7fRvQfa919DaYliYw3SMtjEGFU7V0eo%3D",
        container_name="nileshimagescontainer",
        blob_name=file_name,
        credential=None,
    )

    blob_client.delete_blob()
    return True


delete_blob_client("a1862bbbac594b6685e4d6348b0d9672.jpg")
