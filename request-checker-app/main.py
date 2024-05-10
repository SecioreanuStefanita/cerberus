from fastapi import FastAPI, Request, HTTPException
import json
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse, StreamingResponse
from .crawler_utils.CrawlerCreator import populate_payloads
from .utils.RedisConnection import RedisConnection
from .crawler_utils.CrawlerService import CrawlerService
from fastapi_utilities import repeat_every
import httpx 

redis_client = RedisConnection.get_connection()

if(redis_client == None):
    redis_client = RedisConnection.set_connection()


@repeat_every(seconds=7*60*24)
async def cron_payloads() -> None:
    await populate_payloads(is_on_startup=False)

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
    # Find matching route in configuration
    destination = None
    for route, dest in routing_config.items():
        if url.startswith(route): # type: ignore
            destination = dest
            break

    if destination:
        async with httpx.AsyncClient() as client:
            req = client.build_request(request.method, f"{destination}{path}", content=await request.body(), headers=dict(request.headers))
            resp = await client.send(req, stream=True)

            # Create a FastAPI response from the HTTPX response
            return StreamingResponse(resp.aiter_raw(), status_code=resp.status_code, headers=dict(resp.headers))
    else:
        return JSONResponse(status_code=412, content={}) 



@app.get("/")
def root():
    CrawlerService.count_payload_sizes()
    return {"message": 'Hello'}
