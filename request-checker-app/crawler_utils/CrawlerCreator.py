from .crawlers.PoafCrawler import PoafCrawler
from .CrawlerFactory import CrawlerFactory
from .crawlers.HacktricksCrawler import HacktricksCrawler

class PoatfCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return PoafCrawler()

class HacktricksCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return HacktricksCrawler()