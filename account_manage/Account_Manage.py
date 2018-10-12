from redis import Redis
from redis import BlockingConnectionPool
from config import REDIS_DB, REDIS_PASSWORD, REDIS_HOST




class AccountManage(object):

    def __init__(self):
        self.conn = Redis(connection_pool=BlockingConnectionPool(host=REDIS_HOST, password=REDIS_PASSWORD, db=REDIS_DB))


    def get(self, kname, field):
        return self.conn.hmget(kname, field)

    def getall(self, kname):
        return self.conn.hgetall(kname)

    def hmset(self, kname, value):
        return self.conn.hmset(kname, value)

    def hdel(self, kname, value):
        return self.conn.hdel(kname, value)

    def getone(self, kname):
        results = self.conn.hgetall(kname)
        if results:
            for k,v in results.items():
                return {k: v}
        else:
            return None
