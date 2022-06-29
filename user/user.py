
class User:

    def __init__(self):
        self.__pr_assignee = None
        self.__pr_current = 0
        self.__pr_goal = 0
        self.__pr_total = 0
        self.__pass_yn = None
        self.__warning_cnt = 0
        self.__emojis = None

    # 담당자 
    @property
    def pr_assignee(self):
        return self.__pr_assignee
    
    @pr_assignee.setter
    def pr_assignee(self,pr_assignee):
        self.__pr_assignee=pr_assignee

    # 현재 PR 수
    @property
    def pr_current(self):
        return self.__pr_current
    
    @pr_current.setter
    def pr_current(self,pr_current):
        self.__pr_current=pr_current

    # 목표 PR 수
    @property
    def pr_goal(self):
        return self.__pr_goal
    
    @pr_goal.setter
    def pr_goal(self,pr_goal):
        self.__pr_goal=pr_goal

    # 전체 PR 수
    @property
    def pr_total(self):
        return self.__pr_total
    
    @pr_total.setter
    def pr_total(self,pr_total):
        self.__pr_total+=pr_total 

    # 스프린트 성공여부
    @property
    def pass_yn(self):
        return self.__pass_yn

    @pass_yn.setter
    def pass_yn(self,pass_yn):
        self.__pass_yn=pass_yn


    # 경고 수
    @property
    def warning_cnt(self):
        return self.__warning_cnt

    @warning_cnt.setter
    def warning_cnt(self,warning_cnt):
        self.__warning_cnt=warning_cnt

    # 이모지
    @property
    def emojis(self):
        return self.__emojis

    @emojis.setter
    def emojis(self,emojis):
        self.__emojis=emojis
    

    def info(self):
        content = """>*{0}*
>OPEN_PR   `{1}`/`{2}`
>MERGE_PR  `{3}`
>{4}{5}""".format(self.__pr_assignee,self.__pr_current,self.__pr_goal,self.__pr_total,self.__pass_yn,self.__emojis)
        
        return content



        