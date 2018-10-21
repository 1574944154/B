from redis import Redis
from redis.connection import BlockingConnectionPool
from config import REDIS_DB, REDIS_PASSWORD, REDIS_HOST




class AccountDB(object):

    def __init__(self):
        self.conn = Redis(connection_pool=BlockingConnectionPool(host=REDIS_HOST, password=REDIS_PASSWORD, db=REDIS_DB, decode_responses=True))

    def hmget(self, kname, field):
        return self.conn.hmget(kname, field)

    def hgetall(self, kname):
        return self.conn.hgetall(kname)

    def hmset(self, kname, value):
        return self.conn.hmset(kname, value)

    def hdel(self, kname, value):
        return self.conn.hdel(kname, value)

    def lpop(self, name):
        return self.conn.lpop(name)

    def rpush(self, name, value):
        return self.conn.rpush(name, value)

    def get(self, name):
        return self.conn.get(name)

    def hkeys(self, name):
        return self.conn.hkeys(name)

if __name__ == '__main__':
    conn = AccountDB()
    print(conn.hgetall("complete"))