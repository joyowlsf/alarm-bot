import sqlite3
con = sqlite3.connect("/home/ubuntu/git_info.db")

# PR_INFO 테이블 생성
# con.execute('CREATE TABLE PR_INFO(seq INTEGER PRIMARY KEY NOT NULL,assignee TEXT,title TEXT,status TEXT)')

# USER_INFO 테이블 생성
# con.execute('CREATE TABLE USER_INFO(assignee TEXT,current_pr INTEGER,goal_pr INTEGER,total_pr INTEGER,warning_cnt INTEGER,pass_yn TEXT)')


# con.execute("drop table USER_INFO")

# PR_IFNO 테이블 정보 저장
def pr_info_insert(pr_tuple):
    cur  = con.cursor()
    cur.executemany('INSERT INTO PR_INFO(seq,assignee,title,status) VALUES(?,?,?,?);', pr_tuple)
    con.commit()    
    
# USER_INFO 테이블 정보 저장
def user_info_insert(user_tuple):
    cur  = con.cursor()
    cur.executemany('INSERT INTO USER_INFO VALUES(?,?,?,?,?,?);', user_tuple)
    con.commit()

# 테이블 삭제
def info_delete(query):
    cur = con.cursor()
    cur.execute(query)
    con.commit()

# 테이블 조회
def info_search(query):
    cur  = con.cursor()
    cur.execute(query)

    return cur

# 테이블 수정
def info_update(query):
    cur  = con.cursor()
    cur.execute(query)
    con.commit()


