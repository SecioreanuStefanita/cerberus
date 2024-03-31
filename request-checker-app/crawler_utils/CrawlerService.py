import requests
import msgpack
from ..utils.RedisConnection import RedisConnection
class CrawlerService:
    @staticmethod
    def get_page_content(url, headers, method, params=None, data=None):
        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response;
    
    @staticmethod
    def update_crawler_data(option, values_list):
        redis_client = RedisConnection.get_connection()
        existing_data = msgpack.unpackb(redis_client.get(f'payloads.{option.name}'))
        for value in values_list:
            if value not in existing_data:
                existing_data.append(value)
        redis_client.set(f'payloads.{option.name}', msgpack.packb(existing_data)) # type: ignore
        