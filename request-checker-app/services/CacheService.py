from ..utils.RequestComponentEnum import RequestComponent
import hashlib
import msgpack
import asyncio

class CacheService:
    
    @staticmethod
    async def check_cache_component(hash_key, component_type, cached_requests):
        return hash_key in cached_requests[component_type]

    @staticmethod
    async def check_cache_request(url, path, headers, body, redis_client):
        response = {
            RequestComponent.PATH.name: False,
            RequestComponent.HEADERS.name: False,
            RequestComponent.BODY.name: False
        }

        url_hash = hashlib.md5(f"{url}{path}".encode()).hexdigest()
        headers_hash = hashlib.md5(str(headers).encode()).hexdigest()
        body_hash = hashlib.md5(str(body).encode()).hexdigest()

        cached_requests = msgpack.unpackb(redis_client.get('request_hashes'))

        tasks = [
            asyncio.create_task(CacheService.check_cache_component(url_hash, RequestComponent.PATH.name, cached_requests)),
            asyncio.create_task(CacheService.check_cache_component(headers_hash, RequestComponent.HEADERS.name, cached_requests)),
            asyncio.create_task(CacheService.check_cache_component(body_hash, RequestComponent.BODY.name, cached_requests))
        ]

        results = await asyncio.gather(*tasks)

        response[RequestComponent.PATH.name] = results[0]
        response[RequestComponent.HEADERS.name] = results[1]
        response[RequestComponent.BODY.name] = results[2]

        return response
    
    @staticmethod
    def save_cache_component(component_string, request_component, redis_client):
        cached_requests = msgpack.unpackb(redis_client.get('request_hashes'))
        cached_requests[request_component].append(hashlib.md5(component_string.encode()).hexdigest())
        redis_client.set(f'request_hashes', msgpack.packb(cached_requests)) # type: ignore