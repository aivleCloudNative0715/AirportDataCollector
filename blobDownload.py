import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

# Azure 연결 문자열 (환경 변수 또는 직접 입력 가능)
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AzureWebJobsStorage")


# 다운로드할 로컬 경로
LOCAL_DOWNLOAD_PATH = "./downloaded_blobs"
os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)

# 컨테이너 이름
CONTAINER_NAME = "datacollector"

# 클라이언트 생성
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Blob 목록 조회 및 다운로드
print(f"📦 Downloading blobs from container '{CONTAINER_NAME}'...")
for blob in container_client.list_blobs():
    blob_name = blob.name
    download_path = os.path.join(LOCAL_DOWNLOAD_PATH, os.path.basename(blob_name))

    with open(download_path, "wb") as file:
        blob_data = container_client.download_blob(blob_name)
        file.write(blob_data.readall())
        print(f"✅ Downloaded: {blob_name} → {download_path}")

print("🎉 All blobs downloaded.")
