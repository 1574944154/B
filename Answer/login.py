from selenium import webdriver
from Verification.Verification import CrackGeetest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from account_manage.Account_Manage import AccountDB
from time import sleep
import json
import requests



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Login(object):
	url = "https://passport.bilibili.com/login?gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fhome"
	def __init__(self, username, password):
		self.username = username
		self.password = password
		options = webdriver.ChromeOptions()
		options.add_argument("--no-sandbox")
		# options.add_argument("--headless")
		self.browser = webdriver.Chrome(chrome_options=options)
		self.browser.get(self.url)
		self.conn = AccountDB()
		self.browser.implicitly_wait(20)


	def login(self):
		self.browser.find_element_by_id("login-username").send_keys(self.username)
		self.browser.find_element_by_id("login-passwd").send_keys(self.password)
		for i in range(0, 3):
			if CrackGeetest(self.browser).verify():
				self.conn.hmset("status:"+self.username, {"status": "0"})
				logger.info("verify success")
				# try:
				# 	WebDriverWait(self.browser, 5).until_not(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="login-app"]/div/div[2]/div[3]/div[3]/div/div/ul/li[4]/div/p'), "用户名或密码错误"))
				# except:
				# 	logger.info("密码错误")
				# 	return False
				try:
					WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ser-ul"]/li[1]')))
				except:
					logger.info("登陆异常")
					if "你的账号存在异常，请先验证你的身份" in self.browser.page_source:
						logger.info("账号存在异常，请更改密码")
						self.conn.hmset("status:" + self.username, {"status": "7"})
						return False
					try:
						WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element(
						(By.XPATH, '//*[@id="login-app"]/div/div[2]/div[3]/div[3]/div/div/ul/li[4]/div/p'), "用户名或密码错误"))
					except:
						logger.info("未知错误")
						self.conn.hmset("user", {self.username: self.password})
						return False
					else:
						logger.info("密码错误")
						self.conn.hmset("status:" + self.username, {"status": "4"})
						return False
				self.conn.hmset("user", {self.username: self.password})
				logger.info("登陆成功")
				return True
			else:
				self.browser.refresh()
				logger.info("verify fail")
				self.login()
		self.conn.hmset("user", {self.username: self.password})
		return False

	def get_rcookie(self):
		rcookie = {}
		for cookie in self.browser.get_cookies():
			rcookie[cookie['name']] = cookie['value']
		return rcookie

	def xhw(self):
		"""
		判断答题类型  小黑屋或者会员转正
		:return:
		"""
		url = "https://api.bilibili.com/x/credit/labour/getQs?jsonp=jsonp"
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
		res = requests.get(url, headers=headers, cookies=self.get_rcookie())
		result = json.loads(res.text)
		if result['code'] == 0:
			self.conn.hmset("status:"+self.username, {"type": "2"})
			return True
		else:
			self.conn.hmset("status:"+self.username, {"type": "1"})
			return False







if __name__ == '__main__':
    user = Login("19923393852", "a510b63")
    user.login()