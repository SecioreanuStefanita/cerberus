from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService


class PoafCrawler(Crawler):
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SSTI, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.XSLT, CrawlerOptions.WS, CrawlerOptions.NOSQLI, CrawlerOptions.LFI, CrawlerOptions.PP, CrawlerOptions.CMDI]
   
    
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS.value:
                intial_route = "https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/XSS%20Injection/Intruders"
                content_route = "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/Intruders"
                xss_data = []
                file_names = [ name for name in CrawlerService.get_page_content(intial_route, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'If-None-Match': '*', 'Accept': 'application/json'}, method='GET').json()]
                for file_name in file_names:
                    response = CrawlerService.get_page_content(f"{content_route}/{file_name}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
                    xss_data.extend(response.text.split("\n"))
                self.update(CrawlerOptions.XSS, xss_data)

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


    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)