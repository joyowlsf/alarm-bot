import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("/home/cho/airflow/dags/git-alarm-bot/user")
import user as ur

url = "https://github.com/fubabaz/algorithm/pulls"

response = requests.get(url)

# ur.create()
beom = ur.User()
kyun = ur.User()
spidyweb = ur.User()
zeroradish = ur.User()

def open_crawler():
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find(class_= "js-navigation-container js-active-navigation-container")
        pr = data.find_all(class_ = "d-flex Box-row--drag-hide position-relative")
        
        pr_list = []

        for i in pr:

            pr_assignee = i.find(class_="Link--muted")

            if pr_assignee.get_text() == 'joyowlsf':
                # pr_title = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
                # pr_comment = i.find(class_="text-small text-bold")
                beom.pr_assignee = 'joyowlsf'
                # beom.pr_title = pr_title.get_text()
                # beom.pr_approve_cnt = int(pr_comment.get_text())
                beom.pr_cnt =0
                beom.check()
                
            elif pr_assignee.get_text() == 'kyun-9458':
                # pr_name = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
                # pr_comment = i.find(class_="text-small text-bold")
                kyun.pr_assignee = 'kyun-9458'
                kyun.pr_cnt =1

            elif pr_assignee.get_text() == 'Spidyweb-3588':
                # pr_name = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
                # pr_comment = i.find(class_="text-small text-bold")
                spidyweb.pr_assignee = 'Spidyweb-3588'
                spidyweb.pr_cnt =1

            elif pr_assignee.get_text() == 'zeroradish':
                # pr_name = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
                # pr_comment = i.find(class_="text-small text-bold")
                
                zeroradish.pr_assignee = 'zeroradish'
                zeroradish.pr_cnt =1
                zeroradish.check()

            else:
                zeroradish.pr_assignee = 'zeroradish'
                zeroradish.pr_cnt =0




            # pr_list.append(pr_assignee.get_text())
            
            # pr_name = i.find(class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
            # print(pr_name.get_text())
            # pr_list.append(pr_name.get_text())

            # pr_comment = i.find(class_="text-small text-bold")
            # print(pr_comment.get_text())
            # pr_list.append(pr_comment.get_text())

    else : 
        print(response.status_code)

    return pr_list



if __name__ == "__main__":
    
    open_crawler()
    if zeroradish.pr_assignee == None or beom.pr_assignee == None or spidyweb.pr_assignee == None or kyun.pr_assignee == None:
        zeroradish.pr_assignee = 'zeroradish'
        beom.pr_assignee = 'joywlsf'
        spidyweb.pr_assignee = 'Spidyweb-3588'
        kyun.pr_assignee = 'kyun-9458'

    beom.info()
    kyun.info()
    spidyweb.info()
    zeroradish.info()

    
    