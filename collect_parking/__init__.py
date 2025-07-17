import logging
import azure.functions as func
from shared.collect_parking import collect_parking_data

def main(mytimer: func.TimerRequest) -> None:
    logging.info("🅿️ 주차 정보 수집 중...")
    collect_parking_data()
