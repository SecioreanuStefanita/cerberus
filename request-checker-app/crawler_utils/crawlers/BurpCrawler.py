from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService

class BurpCrawler(Crawler):
    
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.LFI, CrawlerOptions.CMDI]
   
    
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xss_swf_fuzz.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xss_remote_payloads-https.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xss_remote_payloads-http.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xss_payloads_quick.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xss_funny_stored.txt", CrawlerOptions.XSS)
            case CrawlerOptions.LFI:
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/traversal.txt", CrawlerOptions.LFI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/traversal-short.txt", CrawlerOptions.LFI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/lfi.txt", CrawlerOptions.LFI)
            case CrawlerOptions.XEE:
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/xml-attacks.txt", CrawlerOptions.XEE)
            case CrawlerOptions.SQLI:
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/sqli-error-based.txt", CrawlerOptions.SQLI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/sqli-time-based.txt", CrawlerOptions.SQLI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/sqli-union-select.txt", CrawlerOptions.SQLI)
            case CrawlerOptions.CMDI:
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/command_exec.txt", CrawlerOptions.CMDI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/ssi_quick.txt", CrawlerOptions.CMDI)


    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)
        
    def crawl_helper(self, initial_route, option):
        data = []
        response = CrawlerService.get_page_content(f"{initial_route}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
        data.extend(self.parse_page(response.text, initial_route,  option))
          
        self.update(option, data)
        
    def parse_page(self, response, url,  crawler_option):
        data = []
        data.extend(response.strip().split('\n'))
        return data