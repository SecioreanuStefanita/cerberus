import random
from fastapi import FastAPI, Request, HTTPException, Response, Form
import json
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from flask import redirect
from .crawler_utils.CrawlerCreator import populate_payloads
from .utils.RedisConnection import RedisConnection
from .crawler_utils.CrawlerService import CrawlerService
from fastapi_utilities import repeat_every
from .services.CheckerService import CheckerService
from .services.LogsService import LogsService
from typing import Annotated, Optional
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
    await populate_payloads(is_on_startup=False) #TODO: Change this to false after testing is done

app = FastAPI(lifespan=lifespan)

with open("request-checker-app/routing_config.json", "r") as config_file:
    routing_config = json.load(config_file)

needs_honeypot_redirect = False
resource = None

@app.middleware("http")
async def route_middleware(request: Request, call_next):
    global needs_honeypot_redirect, resource
    url = request.url.hostname
    path: str = request.url.path
    destination = None
    honeypot_destination: Optional[str] = None

    if path.startswith("/redirected"):
        return await call_next(request)

    if needs_honeypot_redirect:
        needs_honeypot_redirect = False
        response = RedirectResponse(url=f'/redirected?url={resource}')
        return response

    # Find the destination based on the URL
    for route, dest in routing_config.items():
        if url and url.startswith(route):
            destination = f"{dest['target']}:{dest['port']}"
            honeypot_destination = f"http://127.0.0.1:{dest['honeypot_port']}{dest['honeypot_path']}404"
            break

    if destination:
        is_safe_request = await CheckerService.check_request(destination, path, request.headers, await request.body(), redis_client)
        if is_safe_request:
            async with httpx.AsyncClient() as client:
                req = client.build_request(request.method, f"{destination}{path}", content=await request.body(), headers=dict(request.headers))
                resp = await client.send(req, stream=True)
                return StreamingResponse(resp.aiter_raw(), status_code=resp.status_code, headers=dict(resp.headers))
        else:
            needs_honeypot_redirect = True
            resource = honeypot_destination
            response = RedirectResponse(url=f'/redirected?url={honeypot_destination}')
            return response
    else:
        return JSONResponse(status_code=404, content={'Content Not Found for the specified request'})

@app.api_route("/redirected", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def redirected(request: Request, url: str):
    async with httpx.AsyncClient() as client:
        try:
            if request.method == "GET":
                response = await client.get(url)
            elif request.method == "POST":
                response = await client.post(url, content=await request.body())
            elif request.method == "PUT":
                response = await client.put(url, content=await request.body())
            elif request.method == "DELETE":
                response = await client.delete(url)
            elif request.method == "PATCH":
                response = await client.patch(url, content=await request.body())
            elif request.method == "OPTIONS":
                response = await client.options(url)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type", "text/html"))

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error fetching webpage: {exc.response.text}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(exc)}")


@app.get("/")
def root():
    CrawlerService.count_payload_sizes()
    return {"message": 'Hello'}



app_internal = FastAPI()
@app_internal.post("/logs")
def save_logs(type: Annotated[str, Form()], payload: Annotated[str, Form()]):
    LogsService.save_data(type, payload)
    return {"message": 'Hello'}
