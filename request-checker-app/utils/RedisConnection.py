import redis
from ..crawler_utils.CrawlerOptions import CrawlerOptions
import msgpack

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisConnection( metaclass=Singleton):
    r = None
    
    @staticmethod
    def get_connection():
        if RedisConnection.r == None:
            return RedisConnection.set_connection()
        else:
            return RedisConnection.r
    
    @staticmethod
    def set_connection():
        RedisConnection.r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        data = {option.name: [] for option in CrawlerOptions}
        RedisConnection.r .set('payloads', msgpack.packb(data)) # type: ignore
        return RedisConnection.r