from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from main import scrap

default_args = {
    'owner': 'Hesry_Quentin',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 21),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='Scraping script',
    default_args=default_args,
    description='A DAG that executes the scraping script',
    tags=['scraping'],
    schedule_interval=timedelta(minutes=30)
)

execute_script = PythonOperator(
    task_id='execute_python_script',
    python_callable=scrap,
    dag=dag
)

execute_script
