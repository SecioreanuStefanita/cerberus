from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions

class HacktricksCrawler(Crawler):
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                print("Crawling for XSS")
            case CrawlerOptions.SSTI:
                print("Crawling for SSTI")
            case CrawlerOptions.SQLI:
                print("Crawling for SQLI")
            case CrawlerOptions.XEE:
                print("Crawling for XEE")
            case CrawlerOptions.XSLT:
                print("Crawling for XSLT")
            case CrawlerOptions.WS:
                print("Crawling for WS")
            case CrawlerOptions.NOSQLI:
                print("Crawling for NOSQLI")
            case CrawlerOptions.LFI:
                print("Crawling for LFI")
            case CrawlerOptions.PP:
                print("Crawling for PP")
            case CrawlerOptions.CMDI:
                print("Crawling for CMDI")
            case CrawlerOptions.ALL:
                print("Crawling for ALL")
    def map(self):
        pass
    def cron(self):
        pass
    def update(self):
        pass