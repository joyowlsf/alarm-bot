from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
import pendulum
from datetime import datetime

import sys
sys.path.append("/home/cho/airflow/dags/alarm-bot/crawler")
import open_crawler as op
sys.path.append("/home/cho/airflow/dags/alarm-bot/check")
import pr_check as pr
import user_check as ur


import requests
from bs4 import BeautifulSoup
import re


# OPEN PR 유무 확인
def open_pr_yn():
    url = "https://github.com/fubabaz/algorithm/pulls"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # open pr 갯수 확인
    open_cnt = soup.find(class_="btn-link selected").text
    re_open_cnt = re.sub(r"[^0-9]","",open_cnt.split('\n')[4].replace(" ",""))
    
    return "open_crawler" if int(re_open_cnt) > 0 else "No"


args = {
    "owner" : "airflow",
}


local_tz = pendulum.timezone("Asia/Seoul")

with DAG(
    dag_id="slack-etl",
    default_args = args,
    schedule_interval="0 17 * * *",
    start_date = datetime(2022,6,20, tzinfo=local_tz),
    # schedule_interval="@once",
    catchup=False,
    # dagrun_timeout=timedelta(minutes=5),
    # start_date = days_ago(2),
) as dag:

    t1 = BranchPythonOperator(
        task_id='open_pr_yn',
        python_callable=open_pr_yn,
        dag=dag)

    # OPEN_PR 데이터 수집
    t2 = PythonOperator(
        task_id='open_crawler',
        python_callable=op.open_crawler,
        dag=dag)

    # OPEN_PR DB 적재 및 동기화
    t3 = PythonOperator(
        task_id='pr_check',
        python_callable=pr.pr_check,
        dag=dag)
    
    # PR 정보 DB 적재 및 slack 메시지 전송
    t4 = PythonOperator(
        task_id='slack_send',
        python_callable=ur.slack_send,
        trigger_rule='none_failed_or_skipped',
        dag=dag)



    dummy_1 = DummyOperator(task_id="No")

    t1 >> dummy_1 >> t4
    t1 >> t2 >> t3 >> t4
    