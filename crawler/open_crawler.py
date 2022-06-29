import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('/home/cho/airflow/dags/alarm-bot/load')
import load_to_sqlite3 as sq
import re


# OPEN PR 정보 수집
def open_crawler():
    url = "https://github.com/fubabaz/algorithm/pulls"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # open pr 갯수 확인
    # open_cnt = soup.find(class_="btn-link selected").text
    # re_open_cnt = re.sub(r"[^0-9]","",open_cnt.split('\n')[4].replace(" ",""))

  
    pr_list = []

    # if int(re_open_cnt) > 0:
        
    data = soup.find(class_= "js-navigation-container js-active-navigation-container")
    pr = data.find_all(class_ = "d-flex Box-row--drag-hide position-relative")

    for i in pr:
            
        # pr 번호
        pr_num = i.find(class_="opened-by")
        re_pr_num = re.sub(r"[^0-9]","",pr_num.get_text().split('\n')[1].replace(" ",""))
        pr_list.append(int(re_pr_num))

        # pr 담당자
        pr_assignee = i.find(class_="Link--muted").text
        pr_list.append(pr_assignee)
            
        # pr 제목
        pr_title = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title").text
        pr_list.append(pr_title)

        # pr 상태
        pr_list.append('open')

    # else:
    #     print("OPEN_PR 정보가 없습니다.")

    return pr_list




if __name__ == "__main__":
    open_crawler()

    
    