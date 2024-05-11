from ..utils.RequestComponentEnum import RequestComponent
from ..crawler_utils.CrawlerOptions import CrawlerOptions
import asyncio
import msgpack
from .CacheService import CacheService
class CheckerService:
    @staticmethod
    async def check_request(url, path, headers, body, redis_client):
        cache_response = await CacheService.check_cache_request(url, path, headers, body, redis_client)
        payloads =  msgpack.unpackb(redis_client.get(f'payloads'))
        tasks = []

        if not cache_response[RequestComponent.PATH.name]:
            tasks.append(CheckerService.check_component(RequestComponent.PATH.name, f"{url}{path}", payloads))
        if not cache_response[RequestComponent.HEADERS.name]:
            tasks.append(CheckerService.check_component(RequestComponent.HEADERS.name, str(headers), payloads))
        if not cache_response[RequestComponent.BODY.name]:
            tasks.append(CheckerService.check_component(RequestComponent.BODY.name, str(body), payloads))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            component_type, is_safe, component_data = result # type: ignore
            if is_safe:
                CacheService.save_cache_component(component_data, component_type, redis_client)

        # Determine overall safety based on individual results
        is_safe_path = cache_response[RequestComponent.PATH.name] or any(res[0] == RequestComponent.PATH.name and res[1] for res in results) # type: ignore
        is_safe_headers = cache_response[RequestComponent.HEADERS.name] or any(res[0] == RequestComponent.HEADERS.name and res[1] for res in results) # type: ignore
        is_safe_body = cache_response[RequestComponent.BODY.name] or any(res[0] == RequestComponent.BODY.name and res[1] for res in results) # type: ignore

        return is_safe_path and is_safe_headers and is_safe_body

    @staticmethod
    async def check_component(component_type, component_data, payloads_json):
        async def check_payloads(option):
            for payload in payloads_json[option]:
                if payload in component_data:
                    return False
            return True

        tasks = [check_payloads(option) for option in CrawlerOptions]
        results = await asyncio.gather(*tasks)
        is_safe = all(results)
        return (component_type, is_safe, component_data)
