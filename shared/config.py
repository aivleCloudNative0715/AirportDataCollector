import os
from dotenv import load_dotenv

load_dotenv()

PARKING_API_URL = "http://apis.data.go.kr/B551177/StatusOfParking/getTrackingParking"
ARRIVAL_API_URL = "http://apis.data.go.kr/B551177/statusOfAllFltDeOdp/getFltArrivalsDeOdp"
DEPARTURE_API_URL = "http://apis.data.go.kr/B551177/statusOfAllFltDeOdp/getFltDeparturesDeOdp"

SERVICE_KEY = os.getenv("SERVICE_KEY")

INTERVAL_MINUTES = 5