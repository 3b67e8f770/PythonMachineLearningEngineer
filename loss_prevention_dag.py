from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner' : "data_team",
    'depends_on_past': False,
    'start_date':(2026, 5, 15),
    'retries' : 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'loss_prevention_dag',
    default_args=default_args,
    schedule_interval = "0 0 * * *",
    catchup=False,
    description="daily ETL"
) as dag:
    
    # Krok A: Pusty operator startowy (dobra praktyka wizualna w Airflow)
    start_task = EmptyOperator(task_id='start')
    
    # Krok B: Główne zadanie - odpalenie Twojego skryptu PySpark
    run_pyspark_validation = SparkSubmitOperator(
        task_id='run_data_validation',
        application=r'D:\Python\prepering4battle\FRBS\2026_05_11\process_transactions.py', 
        conn_id='spark_default',
        name='Loss_Prevention_Validation'
    )
   
    # Krok C: Pusty operator końcowy
    end_task = EmptyOperator(task_id='end')

    # 4. Ustawienie kolejności wykonywania (Orkiestracja)
    start_task >> run_pyspark_validation >> end_task