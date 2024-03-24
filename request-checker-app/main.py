from fastapi import FastAPI
from .crawler_utils.CrawlerCreator import PoatfCrawlerFactory

app = FastAPI()

@app.get("/")
def root():
    f = PoatfCrawlerFactory()
    response = f.create_crawler().crawl(1)
    return {"message": response}
