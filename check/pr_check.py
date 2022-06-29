import sys
sys.path.append('/home/cho/airflow/dags/alarm-bot/load')
import load_to_sqlite3 as sq
sys.path.append('/home/cho/airflow/dags/alarm-bot/crawler')
import open_crawler as op
import re
import numpy as np
# sys.path.append('/home/cho/airflow/dags/alarm-bot/user/')]
# import user as ur


# OPEN PR 비교 및 저장
def pr_check():

    # DB에 OPEN PR이 존재하면 1 없으면 0을 반환
    db_open_cnt = sq.info_search("SELECT EXISTS(SELECT 1 FROM PR_INFO WHERE STATUS='open')").fetchone()
    re_db_open_cnt = re.sub(r"[^0-9]","",str(db_open_cnt))
    
    # open_crawler 데이터
    pr_list = op.open_crawler()

    # open_crawler 데이터 numpy
    crawler_data = np.array(pr_list)
    
    # 2차원 배열로 변환
    np_pr_list = crawler_data.reshape((int(len(crawler_data)/4),4))

    # 스프린트 도중 MERGE PR 이 존재하는지 확인
    if int(re_db_open_cnt) == 0:
        # OPEN PR 정보 튜플 전환
        pr_tuple = tuple(np_pr_list)

        # OPEN PR 데이터 저장
        sq.pr_info_insert(pr_tuple)
        print("OPEN PR 데이터 DB에 저장")
    else:

        # DB 데이터 딕셔너리
        db_data = dict(sq.info_search("SELECT seq,assignee FROM PR_INFO WHERE STATUS = 'open'").fetchall())

        # 크롤링 데이터 딕셔너리
        crawler_data_dict = {}

        # 크롤링 데이터 2차원 배열 -> 딕셔너리 변환
        for np_data in (np_pr_list):
            crawler_data_dict[int(np_data[0])] = np_data[1]

   
        db_data_keys = list(db_data.keys())
        crawler_data_dict_keys = list(crawler_data_dict.keys())

        s_db_data_key = set(db_data_keys)
        s_crawler_data_dict_key = set(crawler_data_dict_keys)

        # 바뀐 pr 번호
        d_seq = s_crawler_data_dict_key - s_db_data_key

        # 숫자만 출력
        re_d_seq = re.sub(r"[^0-9]","",str(d_seq))

        # d_assigne = (crawler_data_dict)[int(re_d_seq)]

        if not re_d_seq:
            print("추가로 업로드 PR 및 MERGE PR이 존재하지 않습니다.")
        else:
            print("MERGE PR은 close로 변경합니다.")
            sq.info_update("UPDATE PR_INFO SET STATUS = 'close' WHERE SEQ={0}".format(re_d_seq))


if __name__ == "__main__":
    pr_check()






