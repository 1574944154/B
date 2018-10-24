import json
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from config import MAX_PROCESS, RATE
from Answer.login import Login
from Answer.hyzz_answer import Hyzz_answer
from account_manage.mysql_db import Mysql_db
from Answer.xhw_answer import Xhwanser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def task():
    conn = Mysql_db()
    account = conn.lpop("queue")
    if account:
        username = account[0]
        password = account[1]
        conn.insert_user([username,password])
        user = Login(username, password)
        pass_correct = user.login()
        if pass_correct:
            # 密码正确
            if user.xhw():
                # 小黑屋答题
                logger.info("开始答小黑屋")
                Xhwanser(user.get_rcookie(), username).loop()
                return True
            else:
                # 会员转正答题
                logger.info("开始会员转正答题")
                Hyzz_answer(user.browser, username, password).loop()
                return True
        else:
            # 密码不正确
            logger.info("{}密码不正确".format(username))

    else:
        logger.info("任务队列为空,进入下一个循环")

def run():
    # main()
    sch = BlockingScheduler()
    sch.add_job(task, "interval", seconds=RATE, max_instances=MAX_PROCESS)
    sch.start()


if __name__ == '__main__':
    run()
