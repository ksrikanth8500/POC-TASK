# WeatherIQ – Intelligent Weather Analytics System

WeatherIQ is a full-stack weather data analytics system built in 4 phases. It fetches real-time, forecasted, and historical weather data, stores and processes it, and uses vector embeddings to support Retrieval-Augmented Generation (RAG) for intelligent query responses.

---

## 🌐 Project Architecture

```
                 OpenWeatherMap API
                          |
              --------------------------
              |         |         |    |
        Real-time  Forecast  Historical  Air Quality
              |         |         |    |
              +---------+---------+----+
                        |
                Phase 2: Collectors
                        |
                   PostgreSQL
                        |
                Phase 3: Ingestion
             (Transform + Validation)
                        |
         +--------------+-------------+
         |                            |
  SentenceTransformer           pgvector
         |                            |
         +--------------+-------------+
                        |
              Phase 4: FastAPI RAG API
                        |
                      Client
```

---

## 📂 Folder Structure

```
WeatherIQ/
├── phase1/                              # Infrastructure Setup
│   └── airflow_local/
│       └── dags/
│
├── phase2/                              # Weather Data Collection
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── realtime_collector.py
│   │   ├── historical_collector.py
│   │   ├── forecast_collector.py
│   │   ├── air_quality_collector.py
│   │   └── config.py
│   ├──db/ db.py
│   └── requirements.txt
│
├── phase3/                              # Data Ingestion
│   ├── ingestion/
│   │   ├── transform.py
│   │   ├── validate.py
│   │   └── __init__.py
│   ├── collectors/
│   │   └── realtime_collector.py
│   
│   
│
├── phase4/                              # RAG System
│   ├── api/
│   │   ├── rag_api.py                   # FastAPI application
│   ├── embeddings/
│       ├── embedder.py                 # Embedding generation
│       ├── storage.py                  # pgvector search and storage
│
├── db.py
├── main.py
├── models.py
├── weather_service.py
├── requirements.txt
├── README.md
├── architecture.png                    # Architecture Diagram
└── requirements.txt
```

---

## 🚀 Phase-wise Breakdown

### ✅ Phase 1: Infrastructure
- Setup PostgreSQL with pgvector
- FastAPI base initialized
- Optional: Docker/WSL setup for Airflow

### ✅ Phase 2: Weather Data Collectors
- Fetches real-time, historical, forecast, and air quality data
- Stores raw and structured data into PostgreSQL

### ✅ Phase 3: Ingestion Pipelines
- Uses transformation and validation logic
- Scheduled with Airflow to run ETL jobs

### ✅ Phase 4: RAG System
- SentenceTransformer for embeddings
- pgvector stores & searches embeddings
- FastAPI provides top-3 matching results based on similarity

---

## 👨‍💻 Technologies Used
- FastAPI
- PostgreSQL + pgvector
- Apache Airflow
- SentenceTransformer
- OpenWeatherMap API

---

## ⚙️ Setup Instructions

1. **PostgreSQL Setup**
   - Ensure pgvector extension is installed and enabled
2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run FastAPI**
   ```bash
   uvicorn phase4.api.rag_api:app --reload
   ```
4. **Access Docs**
   - http://127.0.0.1:8000/docs

---

## 🔗 GitHub Repository

### Repository: [WeatherIQ](https://github.com/your-username/WeatherIQ)

Push the project using:
```bash
git init
git remote add origin https://github.com/your-username/WeatherIQ.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

---

