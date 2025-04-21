# airflow_local/dags/phase3_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../phase3')))

from collectors.realtime_collector import fetch_realtime_weather
from ingestion.transform import transform_realtime
from ingestion.validate import is_valid_weather
#from airflow_local.utils.db_writer import write_to_db  # optional util if you want

default_args = {
    'owner': 'phase3',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def collect_transform_store(city):
    data = fetch_realtime_weather(city)
    structured = transform_realtime(data)
    if is_valid_weather(structured):
        print(f"Ingesting {structured}")
        # write_to_db(structured) OR insert here directly
    else:
        print(f"Invalid data for {city}")

with DAG(
        dag_id="phase3_weather_pipeline",
        default_args=default_args,
        schedule_interval="@hourly",
        catchup=False
) as dag:

    for city in ["London", "New York", "Tokyo"]:
        PythonOperator(
            task_id=f"ingest_{city.lower().replace(' ', '_')}",
            python_callable=collect_transform_store,
            op_args=[city]
        )
