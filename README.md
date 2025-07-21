# ✈️ Airport Data Collector

공항 운항정보 및 주차장 현황 데이터를 수집하여 혼잡도 예측, 사용자 안내 챗봇 등에 활용하기 위한 자동화 수집 프로젝트입니다.

## 📌 프로젝트 개요

이 저장소는 다음의 두 가지 주요 데이터를 주기적으로 수집합니다:

1. **항공편 운항 정보**
   - 도착/출발 항공편 데이터
   - 공공 데이터 포털 API 사용
   - 하루 1회 전체 항공편 조회

2. **공항 주차장 현황**
   - 5분 간격 실시간 현황 API 호출
   - 주차장 별 혼잡도 분석에 사용

수집된 데이터는 Azure Blob Storage에 저장됩니다.

---

## 📁 디렉토리 구조
```
AirportDataCollector
├── README.md
├── requirements.txt
├── host.json               # Azure Functions 호스트 설정
├── local.settings.json     # 로컬 개발용 환경 설정
├── flight_data.csv         # 예시 항공편 데이터
├── parking_data.csv        # 예시 주차장 데이터
│
├── collect_fight/ # 항공편 수집 함수 (Azure Function)
│  ├── init.py
│  └── function.json
│
├── collect_parking/ # 주차장 수집 함수 (Azure Function)
│  ├── init.py
│  └── function.json
│
└── shared/ # 공통 로직 모듈
   ├── collect_flight.py
   ├── collect_parking.py
   ├── config.py
   └── utils.py
```
## ⏱ 스케줄 설정

이 프로젝트는 Azure Functions 타이머 트리거를 사용하여 자동 실행됩니다.

- **항공편 수집 (`collect_fight`)**
  - 매일 오전 10시 30분 실행  
  - CRON 스케줄: `"0 0 9 * * *`

- **주차장 수집 (`collect_parking`)**
  - 5분 간격으로 실행  
  - CRON 스케줄: `0 */5 * * * *`

---

## 🔧 실행 환경

- Python 3.10
- Azure Functions Core Tools

### 필수 Python 패키지

```bash
pip install -r requirements.txt
```

---

## 💾 수집 데이터 다운로드 도구

- **📄 파일명**: `blobDownload.py`  
- **🛠 용도**: Azure Blob Storage에 저장된 수집 데이터를 한 번에 로컬로 다운로드하는 스크립트입니다.

### ▶️ 사용법

1. `.env` 파일에 Azure Blob Storage 연결 문자열(`AzureWebJobsStorage`)이 설정되어 있어야 합니다.
2. 의존 패키지를 설치합니다:

   ```bash
   pip install -r requirements.txt
   ```
3. 스크립트를 실행합니다:
    ``` bash
   python blobDownload.py
   ```

4. 다운로드된 파일은 `./downloaded_blobs/` 폴더에 저장됩니다.
