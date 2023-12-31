import os

from google.cloud import storage
from google.oauth2 import service_account

AUTH_FILE = 'auth/anywallpaper-de0f0-85d1324687a0.json'
BUCKET_NAME = 'anywallpaper-wiseart-dev'

storage_cred = service_account.Credentials.from_service_account_file(AUTH_FILE)
storage_client = storage.Client(credentials=storage_cred)
bucket = storage_client.bucket(BUCKET_NAME)


def upload_storage(path: str, destination_blob_name: str):
    try:
        print(f'start upload: {destination_blob_name}')
        blob = bucket.blob(destination_blob_name)
        if blob.exists():
            return destination_blob_name
        generation_match_precondition = 0
        blob.upload_from_filename(path, if_generation_match=generation_match_precondition)
        print(f"File {path} uploaded to {destination_blob_name}")
        return destination_blob_name
    except Exception as e:
        print(e)
        if '"code": 412' in str(e):
            return destination_blob_name
        return None


def upload_files(root_path: str):
    for file_name in os.listdir(root_path):
        if '.DS' in file_name:
            continue
        upload_path = f'{root_path}/{file_name}'
        if os.path.isdir(upload_path):
            upload_files(upload_path)
        else:
            upload_storage(upload_path, upload_path)


if __name__ == '__main__':
    upload_files('foocus_models')
