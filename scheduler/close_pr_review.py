from airflow import DAG
from datetime import datetime, timedelta
# from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pendulum



args = {
    "owner" : "airflow",
}


local_tz = pendulum.timezone("Asia/Seoul")

# 매주 월요일 00시 01분 실행
with DAG(
    dag_id="pr-etl",
    default_args = args,
    schedule_interval="1 0 * * 1",
    start_date = datetime(2022,6,20, tzinfo=local_tz),
    catchup=False,
) as dag:


    # CLOSE_PR 데이터 수집
    t5 = BashOperator(
        task_id='close_crawler',
        bash_command = 'python3 /home/ubuntu/airflow/dags/alarm-bot/crawler/close_crawler.py',
        dag=dag)

t5