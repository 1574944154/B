from redis import Redis
from redis.connection import BlockingConnectionPool
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
import time

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
	conn0 = Redis(connection_pool=BlockingConnectionPool(host="39.106.122.164", db=1, password="yuanjie"))
	conn1 = Redis(connection_pool=BlockingConnectionPool(host="39.106.122.164", db=4, password="yuanjie"))
	results = conn0.hgetall("1")
	for k, v in results.items():
		conn1.hmset("1", {k.decode("utf-8"): v.decode("utf-8")})
		print(k, v)




def test():
	b = webdriver.Chrome()
	b.get("https://www.bilibili.com/video/av12097513")
	with open("source_page.txt", "w", encoding="utf-8") as f:
		f.write(b.page_source)



if __name__ == '__main__':
	move()
