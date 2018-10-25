import requests
import json
import logging
from time import sleep
from account_manage.mysql_db import Mysql_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Xhwanser(object):

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
	}
	url = "https://api.bilibili.com/x/credit/labour/getQs?jsonp=jsonp"

	def __init__(self, cookies, username):
		self.cookies = cookies
		self.session = requests.session()
		self.username = username
		self.headers['Cookie'] = self.cookie_str()
		self.conn = Mysql_db()
		self.conn.set_status(self.username, "1")

	def cookie_str(self):
		cookie_str = ""
		for name, value in self.cookies.items():
			line = name + "=" + value + "; "
			cookie_str += line
		cookie_str = cookie_str[:-2]
		return cookie_str

	def answer(self):
		res = self.session.get(self.url, headers=self.headers, cookies=self.cookies)
		answers = json.loads(res.text)
		if answers['code'] == 0:
			answers = answers['data']
		else:
			logger.info("获取答案异常")

		answerString = ""
		answerIdString = ""
		for answer in answers:
			answerIdString += str(answer['id']) + ","
			ans = self.conn.get_ans("xhw", str(answer['id']))
			if ans:
				answerString += ans+","
			else:
				answerString += "1,"


		answerString = answerString[:-1]
		answerIdString = answerIdString[:-1]
		form_data = {
			"id": answerIdString,
			"ans": answerString,
			"buvid3": self.cookies['buvid3'],
			"csrf": self.cookies['bili_jct'],
			"jsonp": "jsonp"
		}

		res = self.session.post("https://api.bilibili.com/x/credit/labour/commitQs", headers=self.headers, data=form_data)
		result = json.loads(res.text)
		if result['code'] == 0:
			if result['data']['score'] == 100:
				return True
			else:
				return False
		else:
			logger.info("答题失败, code码为{}".format(result['code']))
			return False

	def loop(self):
		n = 0
		while(n<10):
			if self.answer():
				self.conn.set_status(self.username, "10")
				self.conn.set_score(self.username, "xxx")
				logger.info("答题成功")
				return True
			else:
				logger.info("{}次答题不成功，再次答题".format(n))
				sleep(10)
		self.conn.set_status(self.username, "6b")
		logger.info("n次答题不成功，账号退出登陆".format(n))
		return False

if __name__ == '__main__':
	cookies = {"finger": "edc6ecda","buvid3": "5C4C7AB4-D98F-451E-91DF-06458AF7A41013550infoc","LIVE_BUVID": "AUTO3215403812220900","sid": "js3c8l38","DedeUserID": "65713828","DedeUserID__ckMd5": "60c7f449ec0f701e","SESSDATA": "23558a52%2C1542973278%2Cf24b210b","bili_jct": "7b499a19c1e1e3fccd29ac6199d0fe42","_dfcaptcha": "9ba783581def0f53bccb8283193c9b9b"}
	ans = Xhwanser(cookies, "152654")
	ans.loop()