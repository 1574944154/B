from redis import Redis
from redis.connection import BlockingConnectionPool
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import pymysql

def remove():
	conn = Redis(connection_pool=BlockingConnectionPool(host="39.106.122.164", db=1, password="yuanjie"))
	results = conn.hgetall("status")
	remove = []
	for num, code in results.items():
		if code.decode("utf-8") == "6":
			remove.append(num.decode("utf-8"))

	for i in remove:
		conn.hdel("status", i)

def move():
	conn0 = Redis(connection_pool=BlockingConnectionPool(host="39.106.122.164", db=4, password="yuanjie", decode_responses=True))
	db = pymysql.connect(host="127.0.0.1", user="root", password="yuanjie", database="bilibili_account")
	cursor = db.cursor()
	for i in range(1,23000):
		result = conn0.get("bilibili:"+str(i)+":answer")
		if result:
			cursor.execute("INSERT INTO xhw(id,ans) VALUES ('{}','{}')".format(str(i), result))
			db.commit()


def test():
	ss = (('19923393852', '6', 1, 84), ('17080622562', '10', 2, None), ('15683956189', '6', 1, 76))
	for one in ss:
		print(one)



if __name__ == '__main__':
	test()
