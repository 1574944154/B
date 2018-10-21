import requests
import json
import logging
from time import sleep
from account_manage.Account_Manage import AccountDB

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
		self.conn = AccountDB()
		self.conn.hmset("status:" + self.username, {"status": "1"})

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
		print(answers)
		for answer in answers:
			answerIdString += str(answer['id']) + ","
			ans = self.conn.get("bilibili:"+str(answer['id'])+":answer")
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
				self.conn.hmset("status:"+self.username, {"status": "10"})
				self.conn.hmset("complete", {self.username: "xxx"})
				logger.info("答题成功")
				return True
			else:
				logger.info("{}次答题不成功，再次答题".format(n))
				sleep(10)
		self.conn.hmset("status:"+self.username, {"status": "6b"})
		logger.info("n次答题不成功，账号退出登陆".format(n))
		return False

if __name__ == '__main__':
	cookies = {"finger": "edc6ecda","buvid3": "8EC49093-52F7-4CC2-B2DD-9157984E1E4D23112infoc","LIVE_BUVID": "AUTO7615400263398273","sid": "daub972m","DedeUserID": "40881595","DedeUserID__ckMd5": "e9ae6a8b43f1ba19","SESSDATA": "9c80637d%2C1542618359%2C0a7451ce","bili_jct": "eb8e5719856581cdbc9bbd764ea13126","_dfcaptcha": "1987395f30d8c5ad6c722ff0823487c6","im_notify_type_40881595": "0","fts": "1540029077"}
	ans = Xhwanser(cookies, "152654")
	ans.loop()