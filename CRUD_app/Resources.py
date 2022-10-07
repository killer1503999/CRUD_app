import os

key_vault = os.getenv("key_vault")
vault_url = "https://"+key_vault+".vault.azure.net/"
AZURE_APP_BLOB_NAME = os.getenv('AZURE_APP_BLOB_NAME')  # enc variable
AZURE_BLOB_PATH = os.getenv('AZURE_BLOB_PATH')
DBName = os.getenv('DBName')
DB_host = os.getenv('DB_host')

# key_vault = "nileshkeyvault"
# vault_url = "https://"+key_vault+".vault.azure.net/"
# AZURE_APP_BLOB_NAME = "nileshimagescontainer"  # enc variable
# AZURE_BLOB_PATH = "https://assessmentstgacc.blob.core.windows.net/nileshimagescontainer/nileshimagescontainer"
# DBName = "Nilesh_Crud_Database"
# DB_host = "assessmentserverget.database.windows.net"
