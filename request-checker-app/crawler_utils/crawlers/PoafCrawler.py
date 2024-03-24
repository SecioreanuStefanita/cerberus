from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
import requests
from bs4 import BeautifulSoup


class PoafCrawler(Crawler):
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS.value:
                intial_route = 'https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection/Intruders'
                response = requests.get(intial_route)
                soup = BeautifulSoup(response.text, 'html.parser')
                a_links = soup.find_all('a')
                for link in a_links:
                    print(link)
                    if "Intruders" in link and '.txt' in link:
                        print(link)
                return response.text.split("textarea")[1]
            case CrawlerOptions.SSTI.value:
                print("Crawling for SSTI")
            case CrawlerOptions.SQLI.value:
                print("Crawling for SQLI")
            case CrawlerOptions.XEE.value:
                print("Crawling for XEE")
            case CrawlerOptions.XSLT.value:
                print("Crawling for XSLT")
            case CrawlerOptions.WS.value:
                print("Crawling for WS")
            case CrawlerOptions.NOSQLI.value:
                print("Crawling for NOSQLI")
            case CrawlerOptions.LFI.value:
                print("Crawling for LFI")
            case CrawlerOptions.PP.value:
                print("Crawling for PP")
            case CrawlerOptions.CMDI.value:
                print("Crawling for CMDI")
            case CrawlerOptions.ALL.value:
                print("Crawling for ALL")
    def map(self):
        pass
    def cron(self):
        pass
    def update(self):
        pass