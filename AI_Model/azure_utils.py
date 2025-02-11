# azure_utils.py

import os
from azure.storage.blob import BlobServiceClient
from config import AZURE_CON_STRING, AZURE_CONTAINER_NAME

def upload_to_blob_storage(local_file_path, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CON_STRING)
        container_name = AZURE_CONTAINER_NAME

        # 컨테이너 생성 (이미 존재하면 무시)
        try:
            blob_service_client.create_container(container_name)
        except Exception as e:
            if "ContainerAlreadyExists" in str(e) or "The specified container already exists" in str(e):
                pass
            else:
                print(f"컨테이너 생성 중 다른 오류 발생: {e}")

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"✅ 파일이 Blob Storage에 업로드되었습니다. URL: {blob_client.url}")
            return blob_client.url
    except Exception as e:
        print(f"❌ Blob Storage 업로드 오류: {e}")
        return None

def upload_json_to_blob_storage(local_json_path, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CON_STRING)
        container_name = AZURE_CONTAINER_NAME

        try:
            blob_service_client.create_container(container_name)
        except Exception as e:
            if "ContainerAlreadyExists" in str(e) or "The specified container already exists" in str(e):
                pass
            else:
                print(f"컨테이너 생성 중 오류 발생: {e}")

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(local_json_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"✅ JSON 파일이 Blob Storage에 업로드되었습니다. URL: {blob_client.url}")
            return blob_client.url
    except Exception as e:
        print(f"❌ JSON Blob Storage 업로드 오류: {e}")
        return None
