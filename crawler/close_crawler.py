import requests
from bs4 import BeautifulSoup
import re
import sys
sys.path.append('/home/cho/airflow/dags/git-alarm-bot/load')
import load_to_sqlite3 as sq


url = "https://github.com/fubabaz/algorithm/pulls?page={1}&q=is%3Apr+is%3Aclosed"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
post = soup.find('em',attrs={"class": "current"})

# close PR 정보 수집
def close_crawler():
    pr_list = []
    

    for i in range(int(post.get('data-total-pages'))):
        url = "https://github.com/fubabaz/algorithm/pulls?page={}&q=is%3Apr+is%3Aclosed".format(i+1)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find(class_= "js-navigation-container js-active-navigation-container")
        pr = data.find_all(class_ = "d-flex Box-row--drag-hide position-relative")
        
        for i in pr:
            
            # merge 된 pr 정보
            pr_check = i.find(class_="tooltipped tooltipped-e")
            if pr_check.get('aria-label') == "Merged pull request":

                # 담당자
                pr_assignee = i.find(class_="Link--muted")
                
                # pr 제목
                pr_title = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
                
                # pr 번호
                pr_num = i.find(class_="opened-by")
                re_pr_num = re.sub(r"[^0-9]","",pr_num.get_text().split('\n')[1].replace(" ",""))
                
            
                # sq.pr_info_insert(re_pr_num,pr_assignee.get_text(),pr_title.get_text(),'closed')


if __name__ == "__main__":
    # sq.info_delete('PR_INFO')
    # close_crawler()
    sq.info_all_search('PR_INFO')





    
    