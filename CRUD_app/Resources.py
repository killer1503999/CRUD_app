import os

key_vault = os.getenv("key_vault")
vault_url = "https://"+key_vault+".vault.azure.net/"
AZURE_APP_BLOB_NAME = os.getenv('AZURE_APP_BLOB_NAME')
AZURE_BLOB_PATHS = os.getenv('AZURE_BLOB_PATH')
DBName = os.getenv('DBName')
DB_host = os.getenv('DB_host')

# import credentials from app service application settings
DB_username = os.getenv("DBUsername")
DB_password = os.getenv("DBpassword")
Blob_SAS_URL = os.getenv("BlobSAS")
