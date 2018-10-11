from Answer.Answer import Answer
from account_manage.Account_Manage import AccountManage
from multiprocessing import Process

from apscheduler.schedulers.blocking import BlockingScheduler

def main():
    account = AccountManage().getall("bilibili")
    if account:

        for user, pwd in account.items():
            AccountManage().hdel("bilibili", user)
            p = Process(target=Answer(user.decode('utf-8'), pwd.decode('utf-8')).loop())
            p.daemon = True
            p.start()

def run():
    # main()
    sch = BlockingScheduler()
    sch.add_job(main, "interval", seconds=50, max_instances=2)
    sch.start()


if __name__ == '__main__':
    run()
