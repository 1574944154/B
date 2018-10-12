from redis import Redis
from redis.connection import BlockingConnectionPool
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
	conn0 = Redis(connection_pool=BlockingConnectionPool(host="127.0.0.1", db=0, password="yuanjie"))
	conn1 = Redis(connection_pool=BlockingConnectionPool(host="39.106.122.164", db=1, password="yuanjie"))
	results = conn0.hgetall("bilibili")

	for key,value in results.items():
		conn1.hmset('account', {key: value.})


def test():
	try:
		1/1

	except:
		print("错误")
	else:
		print("正确")

if __name__ == '__main__':
	move()
