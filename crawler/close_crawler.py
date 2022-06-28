import requests
from bs4 import BeautifulSoup
import re
import sys
sys.path.append('/home/cho/airflow/dags/alarm-bot/load')
import load_to_sqlite3 as sq
import numpy as np




# close PR 정보 수집
def close_crawler():
    
    url = "https://github.com/fubabaz/algorithm/pulls?page={1}&q=is%3Apr+is%3Aclosed"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # CLOSE 페지수 확인
    post = soup.find('em',attrs={"class": "current"})

    pr_list = []

    for i in range(int(post.get('data-total-pages'))):
        url = "https://github.com/fubabaz/algorithm/pulls?page={}&q=is%3Apr+is%3Aclosed".format(i+1)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find(class_= "js-navigation-container js-active-navigation-container")
        pr = data.find_all(class_ = "d-flex Box-row--drag-hide position-relative")
  
        

        for idx,i in enumerate(pr):
            
            # merge 된 pr 정보
            pr_check = i.find(class_="tooltipped tooltipped-e")
            if pr_check.get('aria-label') == "Merged pull request":

 
                # pr 번호
                pr_num = i.find(class_="opened-by")
                re_pr_num = re.sub(r"[^0-9]","",pr_num.get_text().split('\n')[1].replace(" ",""))
                pr_list.append(int(re_pr_num))

                # 담당자
                pr_assignee = i.find(class_="Link--muted").text
                pr_list.append(pr_assignee)
                
                # pr 제목
                pr_title = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title").text
                pr_list.append(pr_title)
                
                # pr 상태
                pr_list.append('close')

    return pr_list
            
                
if __name__ == "__main__":
    pr_list = close_crawler()

    # close_crawler 데이터 numpy
    crawler_data = np.array(pr_list)
    
    # 2차원 배열로 변환
    np_pr_list = crawler_data.reshape((int(len(crawler_data)/4),4))

    # CLOSE PR 정보 튜플 전환
    pr_tuple = tuple(np_pr_list)

    # CLOSE PR 데이터 저장
    sq.pr_info_insert(pr_tuple)

    print('CLOSE PR 정보 저장 완료')
    print(sq.info_search("SELECT * FROM PR_INFO").fetchall())





    
    