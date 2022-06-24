import sqlite3
con = sqlite3.connect("git_test2.db")

# PR_INFO
# con.execute('CREATE TABLE PR_INFO(seq INTEGER PRIMARY KEY NOT NULL,assignee TEXT,title TEXT,status TEXT)')

# USER_INFO
# con.execute('CREATE TABLE USER_INFO(assignee TEXT,goal_pr INTEGER,open_pr INTEGER,close_pr INTEGER,result TEXT)')



def pr_info_insert(pr_tuple):
    cur  = con.cursor()
    cur.executemany('INSERT INTO PR_INFO(seq,assignee,title,status) VALUES(?,?,?,?);', pr_tuple)
    con.commit()    
    

def user_info_insert(pr_list):
    cur  = con.cursor()
    cur.executemany('INSERT INTO USER_INFO VALUES(?,?,?,?,?);', (pr_list,))
    con.commit()


def info_delete(query2):
    cur = con.cursor()
    cur.execute(query2)
    con.commit()



def info_search(query):
    cur  = con.cursor()
    cur.execute(query)

    return cur



def info_update(query):
    cur  = con.cursor()
    cur.execute(query)
    con.commit()


# def pr_info_insert2():
#     cur  = con.cursor()
#     cur.execute('INSERT INTO PR_INFO(seq,assignee,title,status) VALUES(?,?,?,?);', (223,'Spidyweb-3588','baekjoon: 1427','close'))
#     con.commit()    

# pr_info_insert2()

def info_search2(query):
    cur  = con.cursor()
    cur.execute(query)

    return cur