import requests
import logging
import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta, timezone
from shared.config import PARKING_API_URL, SERVICE_KEY
import os
from azure.storage.blob import BlobServiceClient

def collect_parking_data():
    url = f"{PARKING_API_URL}?serviceKey={SERVICE_KEY}&numOfRows=100&pageNo=1&type=xml"
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    temp_dir = os.getenv("TEMP", "/tmp")
    filename = os.path.join(temp_dir, f"parking_data_{now.strftime('%Y%m%d_%H%M')}.csv")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items = root.find("body").find("items")

        # CSV 저장
        is_new = not os.path.exists(filename)
        with open(filename, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["timestamp", "floor", "parking", "parkingarea"])
            for item in items.findall("item"):
                writer.writerow([
                    timestamp,
                    item.findtext("floor"),
                    item.findtext("parking"),
                    item.findtext("parkingarea"),
                ])
        logging.info(f"[{now}] 🅿️ 주차장 수집 완료")

        # Azure Blob Storage 업로드
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
        container_client = blob_service_client.get_container_client("datacollector")
        if os.path.exists(filename):
            with open(filename, "rb") as data:
                container_client.upload_blob(name=filename, data=data, overwrite=True)
            logging.info(f"[{now}] ☁️ Blob 업로드 완료: {filename}")
        else:
            logging.warning(f"[{now}] ⚠️ {filename} 파일이 존재하지 않아 업로드 생략됨.")

    except Exception as e:
        logging.info(f"[{now}] ❌ 주차장 오류: {e}")
