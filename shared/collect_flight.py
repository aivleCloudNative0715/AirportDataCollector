import logging
import requests
import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta, timezone
from shared.config import SERVICE_KEY
from shared.utils import get_text
import os
from azure.storage.blob import BlobServiceClient

def collect_flights(api_url, direction):
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    search_date = now.strftime("%Y%m%d")
    page = 1
    total_fetched = 0

    temp_dir = os.getenv("TEMP", "/tmp")
    filename = os.path.join(temp_dir,f"flight_data_{now.strftime('%Y%m%d_%H%M')}.csv")
    is_new = not os.path.exists(filename)

    if is_new:
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "flightId", "fid", "airline", "airport", "airportCode",
                "direction", "scheduled", "estimated", "status", "passengerOrCargo",
                "typeOfFlight", "terminalId", "gateNumber", "fstandPosition",
                "chkinRange", "codeshare", "aircraftSubtype", "aircraftRegNo"
            ])

    while True:
        url = (
            f"{api_url}?serviceKey={SERVICE_KEY}"
            f"&pageNo={page}&numOfRows=1000&type=xml"
            f"&searchdtCode=E&searchDate={search_date}"
            f"&searchFrom=0000&searchTo=2400"
            f"&passengerOrCargo=P&tmp1=-&tmp2=-"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            items = root.find("body").find("items")

            if items is None or len(items.findall("item")) == 0:
                break

            with open(filename, "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                for item in items.findall("item"):
                    writer.writerow([
                        timestamp,
                        get_text(item.find("flightId")),
                        get_text(item.find("fid")),
                        get_text(item.find("airline")),
                        get_text(item.find("airport")),
                        get_text(item.find("airportCode")),
                        direction,
                        get_text(item.find("scheduleDatetime")),
                        get_text(item.find("estimatedDatetime")),
                        get_text(item.find("remark")),
                        get_text(item.find("passengerOrCargo")),
                        get_text(item.find("typeOfFlight")),
                        get_text(item.find("terminalId")),
                        get_text(item.find("gateNumber")),
                        get_text(item.find("fstandPosition")),
                        get_text(item.find("chkinRange")),
                        get_text(item.find("codeshare")),
                        get_text(item.find("aircraftSubtype")),
                        get_text(item.find("aircraftRegNo"))
                    ])
                    total_fetched += 1

            page += 1

        except Exception as e:
            logging.info(f"[{timestamp}] ❌ {direction}편 오류: {e}")
            break

    logging.info(f"[{timestamp}] ✅ {direction}편 {total_fetched}건 수집 완료")

    # Azure Blob Storage 업로드
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
        container_client = blob_service_client.get_container_client("datacollector")
        if os.path.exists(filename):
            with open(filename, "rb") as data:
                container_client.upload_blob(name=filename, data=data, overwrite=True)
            logging.info(f"[{now}] ☁️ Blob 업로드 완료: {filename}")
        else:
            logging.warning(f"[{now}] ⚠️ {filename} 파일이 존재하지 않아 업로드 생략됨.")
    except Exception as e:
        logging.info(f"[{timestamp}] ❌ Blob 업로드 오류: {e}")
