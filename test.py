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
		conn1.hmset('account', {key.decode("utf-8"): value.decode("utf-8")})


def test():
	browser = webdriver.Chrome()
	browser.get("https://baidu.com")
	WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="u1"]/a[1]'), '新闻'))
	WebDriverWait(browser, 20).until(EC.alert_is_present)
	print("r")

if __name__ == '__main__':
	test()
