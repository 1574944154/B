import pymysql
import logging
from config import MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST, MYSQL_USER


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mysql_db(object):

	# def __init__(self):
	# 	db = pymysql.connect(host="127.0.0.1", database="bilibili_account", user="root", password="yuanjie")


	def __getconn(self):
		try:
			db = pymysql.connect(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)
			return db
		except Exception as e:
			logger.info("error {}".format(e))

	def query(self, sql):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute(sql)
			return cursor.fetchall()
		except:
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()

	def insert_user(self, dp):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("INSERT INTO user(username,password) VALUES ('{}','{}')".format(dp[0],dp[1]))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()


	def get_ans(self, table, id):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("SELECT ans FROM {} WHERE id='{}'".format(table, id))
			result = cursor.fetchone()
			if result:
				return result[0]
			else:
				return False
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()


	def set_status(self, username, status):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("UPDATE user SET status='{}' WHERE username='{}'".format(status, username))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()


	def set_type(self, username, type):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("UPDATE user SET type={} WHERE username='{}'".format(type, username))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()



	def get_status(self, username):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("SELECT status FROM user WHERE username='{}'".format(username))
			result = cursor.fetchone()
			if result:
				return result[0]
			else:
				return False
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()





	def get_type(self, username):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("SELECT type FROM user WHERE username='{}'".format(username))
			result = cursor.fetchone()
			if result:
				return result[0]
			else:
				return False
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()


	def set_score(self, username, score):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("UPDATE user SET score='{}' WHERE username='{}'".format(score, username))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()


	def del_user(self, username):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("DELETE FROM user WHERE username='{}'".format(username))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()


	def lpop(self, table):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("SELECT username,password FROM {} ORDER BY id LIMIT 1".format(table))
			result = cursor.fetchone()
			if result:
				cursor.execute("DELETE FROM {} ORDER BY id LIMIT 1".format(table))
				db.commit()
				return result
			return None
		except Exception as e:
			logger.info(e)
			return False
		finally:
			cursor.close()
			db.close()



	def rpush(self, table, up):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("INSERT INTO {}(username, password) VALUES ('{}','{}')".format(table,up[0],up[1]))
			db.commit()
			return True
		except:
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()


	def insert(self, table, data):
		db = self.__getconn()
		cursor = db.cursor()
		try:
			cursor.execute("INSERT INTO {}(username, password) VALUES ('{}','{}')".format(table, data['username'], data['password']))
			db.commit()
			return True
		except Exception as e:
			logger.info(e)
			db.rollback()
			return False
		finally:
			cursor.close()
			db.close()

if __name__ == '__main__':
	print(Mysql_db().query("SELECT username,status,type,score FROM user ORDER BY id DESC"))