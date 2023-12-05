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
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(path)
        print(f"File {path} uploaded to {destination_blob_name}")
        return destination_blob_name
    except Exception as e:
        print(e)
        if '"code": 412' in str(e):
            return destination_blob_name
        return None


if __name__ == '__main__':
    for file_name in os.listdir('files'):
        if '.DS' in file_name:
            continue
        upload_path = f'files/{file_name}'
        if os.path.isdir(upload_path):
            for inner_file in os.listdir(upload_path):
                if '.DS' in inner_file:
                    continue
                inner_path = f'{upload_path}/{inner_file}'
                upload_storage(inner_path, f'foocus_models/{file_name}/{inner_file}')
        else:
            upload_storage(upload_path, f'foocus_models/{file_name}')
