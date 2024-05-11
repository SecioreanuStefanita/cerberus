import redis
from ..crawler_utils.CrawlerOptions import CrawlerOptions
from .RequestComponentEnum import RequestComponent
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
        try:
            existing_data_payloads = msgpack.unpackb(RedisConnection.r.get(f'payloads'))
            existing_data_caches = msgpack.unpackb(RedisConnection.r.get(f'request_hashes'))
            return RedisConnection.r
        except:
            data_payloads = {option.name: [] for option in CrawlerOptions}
            data_caches = {option.name: [] for option in RequestComponent}
            RedisConnection.r .set('payloads', msgpack.packb(data_payloads)) # type: ignore
            RedisConnection.r .set('request_hashes', msgpack.packb(data_caches)) # type: ignore
            return RedisConnection.r
            
    @staticmethod
    def reset_request_cache():
        data_caches = {option.name: [] for option in RequestComponent}
        RedisConnection.r .set('request_hashes', msgpack.packb(data_caches)) # type: ignore
      