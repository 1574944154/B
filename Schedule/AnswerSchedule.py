from Answer.Answer import Answer
from account_manage.Account_Manage import AccountManage
from multiprocessing import Process

from apscheduler.schedulers.blocking import BlockingScheduler
from config import MAX_PROCESS, RATE, ACCOUNT_DB_NAME

def main():
    account = AccountManage().getall(ACCOUNT_DB_NAME)
    if account:

        for user, pwd in account.items():
            AccountManage().hdel(ACCOUNT_DB_NAME, user)
            p = Process(target=Answer(user.decode('utf-8'), pwd.decode('utf-8')).loop())
            p.daemon = True
            p.start()

def run():
    # main()
    sch = BlockingScheduler()
    sch.add_job(main, "interval", seconds=RATE, max_instances=MAX_PROCESS)
    sch.start()


if __name__ == '__main__':
    run()
