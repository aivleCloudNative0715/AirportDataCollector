import logging
import azure.functions as func
from datetime import datetime
from shared.collect_flight import collect_flights
from shared.config import ARRIVAL_API_URL, DEPARTURE_API_URL

def main(mytimer: func.TimerRequest) -> None:
    today = datetime.now().strftime("%Y-%m-%d")

    schedule_status = mytimer.schedule_status or {}
    last = schedule_status.get("last")

    if last is None or last[:10] != today:  # 날짜 문자열 비교
        logging.info("✈️ 항공편 정보 수집 중...")
        collect_flights(ARRIVAL_API_URL, "도착")
        collect_flights(DEPARTURE_API_URL, "출발")

