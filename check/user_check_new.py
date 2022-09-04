import sys
sys.path.append('/home/ubuntu/airflow/dags/alarm-bot/load')
import load_to_sqlite3 as sq
sys.path.append('/home/ubuntu/airflow/dags/alarm-bot/crawler')
import open_crawler as op
sys.path.append('/home/ubuntu/airflow/dags/alarm-bot/user')
import user as ur
import re
import numpy as np
from slack_sdk import WebClient
import datetime as dt

client = WebClient(token='[토큰입력]')


def user_check(user_name):
    # 크롤링 데이터 수집
    user_data = op.open_crawler()

    user_list = []

    # 현재 PR
    pr_current = user_data.count(user_name)

    # 목표 PR
    pr_goal = 1
    
    # 전체 PR
    pr_total = int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT COUNT(*) FROM PR_INFO WHERE STATUS ='close' AND ASSIGNEE='{0}'".format(user_name)).fetchall())))

    #현재 요일
    day = dt.datetime.today().weekday()

    # user 객체 생성
    user = ur.User()

    # 현재 PR 유무 체크
    if pr_current >= pr_goal:
        user.pr_assignee = user_name
        user.pr_current = pr_current
        user.pr_total = pr_total
        user.pr_goal = pr_goal
        user.pass_yn = 'PASS'
        user.warning_cnt = 0
        user.emojis = ":clapping:"
        sq.info_update("UPDATE USER_INFO SET WARNING_CNT = 0 WHERE ASSIGNEE='{0}'".format(user.pr_assignee))
    else:
        user.pr_assignee = user_name
        user.pr_current = pr_current
        user.pr_goal = pr_goal
        user.pr_total = pr_total
        user.pass_yn = 'PROGRESS'
        user.emojis = ":watching-you:"
        
    
    # USER 매일 정보 업데이트
    sq.info_update("UPDATE USER_INFO SET CURRENT_PR = {0}, GOAL_PR = {1}, TOTAL_PR = {2}, PASS_YN ='{3}', WARNING_CNT=WARNING_CNT+{5} WHERE ASSIGNEE='{4}'"
    .format(user.pr_current,user.pr_goal,user.pr_total,user.pass_yn,user.pr_assignee,user.warning_cnt))

    
    #매주 월요일에 순의 체크
    if day == 0:
        if int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT current_pr FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall()))) < pr_goal:
            user.pass_yn = 'FAIL'
            user.emojis = ":facepalm:"
            user.warning_cnt += 1
            sq.info_update("UPDATE USER_INFO SET WARNING_CNT = WARNING_CNT+1 WHERE ASSIGNEE='{0}'".format(user.pr_assignee,user.warning_cnt))
        else:
            print("PASS")
            

    # Faild 정하기
    user.rank = ':alert:'* int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT warning_cnt FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall())))
    
    # 1등 정하기
    if int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT MAX(total_pr) FROM user_info").fetchall()))) == int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT TOTAL_PR FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall()))):
        user.rank = ':trophy_:'
    
    # slack 메시지 전송
    client.chat_postMessage(channel='#4op',text=user.info())


def slack_send():
    days = ['D-6','D-5','D-4','D-3','D-2','D-1','D-day']
    a = dt.datetime.today().weekday()

    client.chat_postMessage(channel='#4op',text="""*ALGORITHM* - *{0}*  
    :sonic: _PR 일정이 존재하는 주의 일요일 23시59분까지 팀원의 PR 리뷰를 진행해주세요. 리뷰가 완료되면 월요일 24시01분에 MERGE 진행하고 정리합니다._:sonic:"""
    .format(days[a]))
    user_check('Spidyweb-3588')
    user_check('joyowlsf')
    user_check('kyun-9458')
    user_check('zeroradish')

