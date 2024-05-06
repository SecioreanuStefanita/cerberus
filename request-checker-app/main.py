from fastapi import FastAPI
from .crawler_utils.CrawlerCreator import populate_payloads
from .utils.RedisConnection import RedisConnection
from .crawler_utils.CrawlerService import CrawlerService
import schedule


app = FastAPI()
redis_client = RedisConnection.get_connection()

if(redis_client == None):
    redis_client = RedisConnection.set_connection()
populate_payloads()

schedule.every(10).seconds.do(populate_payloads)



@app.get("/")
def root():
    CrawlerService.count_payload_sizes()
    return {"message": 'Hello'}
