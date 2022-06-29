import sys
sys.path.append('/home/cho/airflow/dags/alarm-bot/load')
import load_to_sqlite3 as sq
sys.path.append('/home/cho/airflow/dags/alarm-bot/crawler')
import open_crawler as op
sys.path.append('/home/cho/airflow/dags/alarm-bot/user')
import user as ur
import re
import numpy as np
from slack_sdk import WebClient
import datetime as dt

client = WebClient(token=[slack_token])


def user_check(user_name):
    # 크롤링 데이터 수집
    user_data = op.open_crawler()

    user_list = []

    # 현재 PR
    pr_current = user_data.count(user_name)

    # 목표 PR
    pr_goal = int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT goal_pr FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall())))

    # 전체 PR
    pr_total = int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT COUNT(*) FROM PR_INFO WHERE STATUS ='close' AND ASSIGNEE='{0}'".format(user_name)).fetchall())))

    # user 객체 생성
    user = ur.User()

    
    if pr_current >= pr_goal:
        user.pr_assignee = user_name
        user.pr_current = pr_current
        user.pr_goal = pr_goal
        user.pr_total = pr_total
        user.pass_yn = 'PASS'
        user.warning_cnt = 0
        user.emojis = ":sonicdance_pbjtime:"
        sq.info_update("UPDATE USER_INFO SET WARNING_CNT = 0 WHERE ASSIGNEE='{0}'".format(user.pr_assignee))
    else:
        user.pr_assignee = user_name
        user.pr_current = pr_current
        user.pr_goal = pr_goal
        user.pr_total = pr_total
        user.pass_yn = 'FAIL'
        user.warning_cnt = 1
        user.emojis = ":watching-you:"
        
    
    # user_tuple = (user_name,pr_current,pr_goal,pr_total,user.pass_yn,user.warning_cnt)
    
    # USER 매일 정보 업데이트
    sq.info_update("UPDATE USER_INFO SET CURRENT_PR = {0}, GOAL_PR = {1}, TOTAL_PR = {2}, PASS_YN ='{3}', WARNING_CNT=WARNING_CNT+{5} WHERE ASSIGNEE='{4}'"
    .format(user.pr_current,user.pr_goal,user.pr_total,user.pass_yn,user.pr_assignee,user.warning_cnt))

    # 경고 카운트
    warning_cnt = int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT WARNING_CNT FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall())))
    
    # 경고 카운트 6번 시 스프린트 실패, GOAL_PR 2개 추가
    if warning_cnt == 6:
        sq.info_update("UPDATE USER_INFO SET GOAL_PR = GOAL_PR+2 WHERE ASSIGNEE='{0}'".format(user.pr_assignee))
        sq.info_update("UPDATE USER_INFO SET WARNING_CNT = 0 WHERE ASSIGNEE='{0}'".format(user.pr_assignee))
    else:
        sq.info_update("UPDATE USER_INFO SET GOAL_PR = 1 WHERE ASSIGNEE='{0}'".format(user.pr_assignee))

    # 바뀐 목표 PR 조회
    pr_goal = int(re.sub(r"[^0-9]","",str(sq.info_search("SELECT goal_pr FROM USER_INFO WHERE ASSIGNEE='{0}'".format(user_name)).fetchall())))
    # 최종 목표 PR
    user.pr_goal = pr_goal

    # slack 메시지 전송
    client.chat_postMessage(channel='#06_alarm',text=user.info())

    
    # USER 데이터 저장
    # sq.user_info_insert(user_tuple)

def slack_send():
    date = dt.datetime.now()

    client.chat_postMessage(channel='#06_alarm',text="""*ALGORITHM* - *{0}*  
    :sonic: _PR 일정이 존재하는 주의 일요일 오전까지 팀원의 PR 리뷰를 진행해주세요. 리뷰가 완료되면 일요일 오후에 MERGE 진행하고 정리합니다._:sonic:"""
    .format(date.strftime("%A")))
    user_check('Spidyweb-3588')
    user_check('joyowlsf')
    user_check('kyun-9458')
    user_check('zeroradish')







