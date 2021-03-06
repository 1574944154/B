from selenium import webdriver
from Verification.Verification import CrackGeetest
from lxml import etree
import re
import logging
from account_manage.mysql_db import Mysql_db
from time import sleep
from random import randint
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from config import DOWNLOAD_PIC, CLICK_SPEED
from MD5.get_md5 import Update_md5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Hyzz_answer(object):

	def __init__(self, browser, username, password):
		self.conn = Mysql_db()
		self.browser = browser
		self.username = username
		self.password = password
		self.browser.get("http://account.bilibili.com/answer/base/#/")
		self.browser.implicitly_wait(10)


	def click(self, i, j):
		try:
			self.browser.find_element_by_xpath(
				'//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[{}]/ul/li[{}]'.format(i, j)).click()
			logging.info("点击{}、{}".format(i, j))
		except:
			logger.warning("点击{}、{}出错".format(i, j))
		sleep(randint(CLICK_SPEED-2, CLICK_SPEED+2))

	def download(self, url, num):
		with open("./pic/{}/{}".format(num, url[49:-35]), "wb") as f:
			f.write(requests.get(url[17:-35], headers={
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
			}).content)
		logging.info("下载图片{}/{}".format(num, url[49:-35]))

	def findout(self, url, num=1):
		md5 = Update_md5(url[17:-35]).getFileMD5()
		if(num==1):
			table = "ans1_api"
		elif(num==3):
			table = "ans3_api"
		print(md5)
		try:
			ans = self.conn.get_ans(table, md5)
			if ans=='A':
				ans=1
			elif ans=='B':
				ans=2
			elif ans=='C':
				ans=3
			elif ans=='D':
				ans=4
		except:
			logger.error("获取答案失败")
			self.browser.quit()
			return False

		if ans:
			return ans
		else:
			# print(url[17:-35])
			if DOWNLOAD_PIC:
				self.download(url, num)
			return 1

	def one(self):
		logger.info("卷一：社区规范题（第一部分）")
		selector = etree.HTML(self.browser.page_source)
		results = selector.xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li/div/div[2]/@style')
		for index, url in enumerate(results, 1):
			# md5 = result[49:-39]
			self.click(index, self.findout(url))

		self.browser.find_element_by_css_selector(".footer-bottom").click()
		# input("：")
		# 保存错误的图片
		sleep(3)
		self.browser.implicitly_wait(4)
		selector = etree.HTML(self.browser.page_source)
		results = selector.xpath(
			'//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[@class="exam-list error"]/div/div[2]/@style')

		logger.debug("len(results)={}".format(len(results)))
		if len(results) != 0:
			for url in results:
				self.download(url, 1)

			current_url = self.browser.current_url
			logger.debug(current_url)
			# 重新选择正确答案
			while (self.browser.current_url == current_url):
				if re.findall("手机", self.browser.page_source, re.S):
					logger.info("请绑定手机号码")
					self.conn.set_status(self.username, "4")
					self.browser.quit()
					return False
				try:
					self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div/div[2]/div[2]/div').click()
					sleep(5)
					self.browser.implicitly_wait(10)
					results = self.browser.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[@class="exam-list error"]/ul/li[@class=""]')
					for ele in results:
						ele.click()
						sleep(2)
				except:
					# 确定按钮
					self.browser.find_element_by_css_selector(".footer-bottom").click()
					sleep(5)
					self.browser.implicitly_wait(10)
					if re.findall("手机", self.browser.page_source, re.S):
						logger.info("请绑定手机号码")
						self.conn.set_status(self.username, "4")
						self.browser.quit()
						return False

				else:
					current_url = self.browser.current_url
					self.browser.implicitly_wait(2)


	def two(self):
		logger.info("卷一：社区规范题（第二部分）")
		for i in range(1, 11):
			self.click(i, 2)
		# input("：")
		if len(etree.HTML(self.browser.page_source).xpath(
				'//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li/ul/li[@class="active"]')) == 10:
			self.browser.find_element_by_css_selector(".footer-bottom").click()
			sleep(8)
			try:
				WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[6]/ul/li')))
			except:
				self.browser.refresh()

	def three(self):
		logger.info("自选题--选题")
		self.browser.implicitly_wait(4)
		# 选题自选题科目
		self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[3]/ul/li[1]').click()
		sleep(1)
		self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[3]/ul/li[6]').click()
		sleep(1)
		self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li[3]/ul/li[9]').click()
		sleep(1)
		# self.browser.find_element_by_css_selector(".btn-width").click()
		# sleep(1)
		# self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div/div/div/div/p/a').click()
		# sleep(2)
		# self.browser.implicitly_wait(15)
		#
		# selector = etree.HTML(self.browser.page_source)
		# results = selector.xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li/div/div[2]/@style')
		# for index, url in enumerate(results, 1):
		# 	# md5 = result[49:-39]
		# 	self.click(index, self.findout(url, 3))
		self.browser.find_element_by_css_selector(".btn-width[data-v-0b9f0cb2]").click()
		sleep(2)
		try:
			WebDriverWait(self.browser, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/p[1]')))
		except:
			return False

	def threeb(self):
		self.browser.implicitly_wait(10)
		selector = etree.HTML(self.browser.page_source)
		results = selector.xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li/div/div[2]/@style')
		for index, url in enumerate(results, 1):
			# md5 = result[49:-39]
			self.click(index, self.findout(url, 3))
		self.browser.find_element_by_css_selector(".footer-bottom").click()
		sleep(15)
		try:
			WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]')))
		except:
			return False


	def loop(self):

		count = 0
		try:
			while (count<10):
				self.browser.implicitly_wait(15)
				# WebDriverWait(self.browser, 10).until_not(EC.text_to_be_present_in_element(By.XPATH, '//*[@id="app"]/div[2]/div[3]/div/div[2]/div[1]/div/div'))

				html = self.browser.page_source
				selector = etree.HTML(html)
				try:
					alert = selector.xpath('//*[@id="app"]/div[2]/div[3]/div/div[2]/div[1]/div/div')[0].text
				except:
					logger.info("{}未检测到弹窗".format(self.username))
				else:
					if "服务器出错" in alert:
						self.browser.refresh()
						logger.info("{}服务器出错，刷新中.....".format(self.username))
					elif "未绑定手机号" in alert:
						self.conn.set_status(self.username, "4")
						logger.error("{}未绑定手机号码".format(self.username))
						self.browser.quit()
						return False
					elif "12小时内无法再次答题" in alert:
						self.conn.set_status(self.username, "8")
						logger.error("{}12小时无法答题".format(self.username))
						self.browser.quit()
						return False

				# 题目的个数
				select = len(selector.xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div/ul/li'))


				if re.findall("卷一：社区规范题（第一部分）", html, re.S) and select == 40:
					self.conn.set_status(str(self.username), "1b")
					logger.info("{}第一阶段".format(self.username))
					self.one()
					self.conn.set_status(self.username, "1")

				# 二阶段
				elif re.findall("卷一：社区规范题（第二部分）", html, re.S) and select == 10:
					self.conn.set_status(self.username, "2b")
					logger.info("{}第二阶段".format(self.username))
					self.two()
					self.conn.set_status(self.username, "2")

				# 第三阶段
				elif re.findall("军事", html, re.S) and re.findall("物理", html, re.S):
					self.conn.set_status(self.username, "3b")
					logger.info("{}第三阶段".format(self.username))
					self.three()
					self.conn.set_status(self.username, "3")

				elif re.findall("自选题", html, re.S) and select == 50:
					self.conn.set_status(self.username, "3b")
					logger.info("{}第三阶段".format(self.username))
					self.threeb()
					self.conn.set_status(self.username, "3")

				# 最后验证阶段
				elif re.findall("恭喜!你的答案已提交", html, re.S):
					logging.info("验证")
					self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]').click()

					sleep(1)
					self.browser.implicitly_wait(5)
					for i in range(0, 3):
						if CrackGeetest(self.browser).verify():
							ActionChains(self.browser).move_to_element(
								self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/span'))
							logging.info("验证成功")
							self.conn.set_status(self.username, "6b")
							self.browser.find_element_by_css_selector('.btn-width[data-v-71b9c235]').click()
							sleep(15)
							WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[1]/div/div/div/div[3]/span')))
							try:
								score = etree.HTML(self.browser.page_source).xpath('//*[@id="app"]/div[2]/div[1]/div/div/div/div[3]/span/i[2]/text()')[0]
								logger.info("{}分数为：{}".format(self.username, score))
								self.conn.set_score(self.username, score)
								self.conn.set_status(self.username, "6")
							except:
								logger.info("读取分数失败")
							self.browser.quit()
							return True
							# self.conn.set_status(self.username, "6")
							# self.conn.set_score("99")
						else:
							self.browser.refresh()
							self.browser.implicitly_wait(5)
							self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]').click()
							self.browser.implicitly_wait(5)
					self.conn.set_status(self.username, "5")
					self.browser.refresh()
					logger.info("错误")

					count += 1
					logger.info("count={}".format(count))


		except Exception as e:
			self.browser.quit()
			self.conn.rpush("queue", [self.username, self.password, ""])
			logger.error("异常退出{}".format(e))
			return False

		self.conn.set_status(self.username, "7")
		self.browser.quit()
		logger.info("超时")
		return False

''
if __name__ == '__main__':
	a = Hyzz_answer("15212532361", "12345qwe.")
	a.loop()
