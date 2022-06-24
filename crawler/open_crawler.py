import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('/home/cho/airflow/dags/git-alarm-bot/load')
import load_to_sqlite3 as sq
sys.path.append('/home/cho/airflow/dags/git-alarm-bot/check')
import check as ch
import re

url = "https://github.com/fubabaz/algorithm/pulls"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

pr_list= []

# OPEN PR 정보 수집
def open_crawler():
    # open pr 갯수 확인
    open_cnt = soup.find(class_="btn-link selected").text
    re_open_cnt = re.sub(r"[^0-9]","",open_cnt.split('\n')[4].replace(" ",""))

    pr_dict= {}

    if int(re_open_cnt) > 0:
        
        data = soup.find(class_= "js-navigation-container js-active-navigation-container")
        pr = data.find_all(class_ = "d-flex Box-row--drag-hide position-relative")

        for i in pr:
            # pr 담당자
            pr_assignee = i.find(class_="Link--muted").text
            pr_list.append(pr_assignee)
            
            # pr 제목
            pr_title = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title").text
            pr_list.append(pr_title)

            # pr 번호
            pr_num = i.find(class_="opened-by")
            re_pr_num = re.sub(r"[^0-9]","",pr_num.get_text().split('\n')[1].replace(" ",""))
            pr_list.append(re_pr_num)

            # dict 변환
            pr_dict[int(re_pr_num)] = pr_assignee
    else:
        print("OPEN_PR 정보가 없습니다.")

    return pr_dict



# OPEN PR 변동사항 확인
def open_change():
    db_open_cnt = sq.open_info_search("SELECT EXISTS(SELECT 1 FROM PR_INFO WHERE STATUS='open')")
    re_db_open_cnt = re.sub(r"[^0-9]","",str(db_open_cnt))
    
    for i in pr_list:
        sq.pr_info_insert(re_pr_num,pr_assignee.get_text(),pr_title.get_text(),'open')

    
    # if int(re_db_open_cnt) == 0:
    #     # 데이터 저장
    #     sq.pr_info_insert(re_pr_num,pr_assignee.get_text(),pr_title.get_text(),'open')
    # else:
    #     # DB 정보와 비교 후 MERGE PR 존재시 'close' 변환
    #     ch.check()


if __name__ == "__main__":
    # sq.info_delete('PR_INFO')
    open_crawler()
    open_change()

    
    