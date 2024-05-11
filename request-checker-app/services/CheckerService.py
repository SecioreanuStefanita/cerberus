from ..utils.RequestComponentEnum import RequestComponent
from .CacheService import CacheService
class CheckerService():
    @staticmethod
    async def check_request(url, path, headers, body, redis_client):
        is_safe_request = True
        cache_response =  await CacheService.check_cache_request(url, path, headers, body, redis_client)
        
        return is_safe_request

    
   