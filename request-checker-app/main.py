from fastapi import FastAPI, Request, HTTPException, Response
import json
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse, StreamingResponse
from .crawler_utils.CrawlerCreator import populate_payloads
from .utils.RedisConnection import RedisConnection
from .crawler_utils.CrawlerService import CrawlerService
from fastapi_utilities import repeat_every
from .services.CheckerService import CheckerService
import httpx 

redis_client = RedisConnection.get_connection()

if(redis_client == None):
    redis_client = RedisConnection.set_connection()


@repeat_every(seconds=7*60*60*24)
async def cron_payloads() -> None:
    await populate_payloads(is_on_startup=False)
    
@repeat_every(seconds=60*60*24)
async def cron_reset_caches() -> None:
    RedisConnection.reset_request_cache()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await populate_payloads(is_on_startup=True)
    yield
    await populate_payloads(is_on_startup=True) #TODO: Change this to false after testing is done

app = FastAPI(lifespan=lifespan)

with open("request-checker-app/routing_config.json", "r") as config_file:
    routing_config = json.load(config_file)

@app.middleware("http")
async def route_middleware(request: Request, call_next):
    url = request.url.hostname
    path: str = request.url.path
    destination = None
    for route, dest in routing_config.items():
        if url.startswith(route): # type: ignore
            destination = dest
            break
    is_safe_request = await CheckerService.check_request(destination, path, request.headers,await request.body(), redis_client)
    if destination:
        if is_safe_request:
            async with httpx.AsyncClient() as client:
                req = client.build_request(request.method, f"{destination}{path}", content=await request.body(), headers=dict(request.headers))
                resp = await client.send(req, stream=True)
                return StreamingResponse(resp.aiter_raw(), status_code=resp.status_code, headers=dict(resp.headers))
        else:
            return JSONResponse(status_code=418, content={'UNDER CONSTRUCTION /  SEND TO HONEYPOT'})
    else:
        return JSONResponse(status_code=404, content={'Content Not Found for the specified request'})



@app.get("/")
def root():
    CrawlerService.count_payload_sizes()
    return {"message": 'Hello'}
