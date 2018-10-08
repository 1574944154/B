from redis import Redis
from redis import BlockingConnectionPool




class AccountManage(object):

    def __init__(self):
        self.conn = Redis(connection_pool=BlockingConnectionPool(host="127.0.0.1", password="yuanjie", db=1))


    def get(self, kname, field):
        return self.conn.hmget(kname, field)

    def getall(self, kname):
        return self.conn.hgetall(kname)

    def hmset(self, kname, value):
        return self.conn.hmset(kname, value)

    def hdel(self, kname, value):
        return self.conn.hdel(kname, value)