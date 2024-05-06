from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService

class FoospidyCrawler(Crawler):
    
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SSTI, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.LFI, CrawlerOptions.CMDI]
   
   
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/jbrofuzz/xss.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/xss/common.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/xss/discovery.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/xss/full.txt", CrawlerOptions.XSS)
                self.crawl_helper("https://github.com/foospidy/payloads/tree-commit-info/master/other/xss", CrawlerOptions.XSS)       
            case CrawlerOptions.SSTI:
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/other/codeinjection/fede.txt", CrawlerOptions.SSTI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/other/codeinjection/struts.txt", CrawlerOptions.SSTI)
            case CrawlerOptions.LFI:
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/jbrofuzz/iis_cgi.txt", CrawlerOptions.LFI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/directory_traversal/deep_traversal.txt", CrawlerOptions.LFI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/directory_traversal/directory_traversal.txt", CrawlerOptions.LFI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/other/traversal/dotdotpwn.txt", CrawlerOptions.LFI)
            case CrawlerOptions.XEE:
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/xss/xml.txt", CrawlerOptions.XEE)
            case CrawlerOptions.SQLI:
                self.crawl_helper("https://github.com/foospidy/payloads/tree-commit-info/master/other/sqli", CrawlerOptions.SQLI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/jbrofuzz/sqli.txt", CrawlerOptions.SQLI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/sqli/sqli.txt", CrawlerOptions.SQLI)
                self.crawl_helper("https://raw.githubusercontent.com/1N3/IntruderPayloads/master/FuzzLists/sqli-union-select.txt", CrawlerOptions.SQLI)
            case CrawlerOptions.CMDI:
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/owasp/fuzzing_code_database/ssi/ssi.txt", CrawlerOptions.CMDI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/other/commandinjection/ismailtasdelen-unix.txt", CrawlerOptions.CMDI)
                self.crawl_helper("https://raw.githubusercontent.com/foospidy/payloads/master/other/commandinjection/ismailtasdelen-windows.txt", CrawlerOptions.CMDI)



          

    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)
        
    def crawl_helper(self, initial_route, option):
        data = []
        if '.txt' not in initial_route:
            file_names = [ name for name in CrawlerService.get_page_content(initial_route, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'If-None-Match': '*', 'Accept': 'application/json'}, method='GET').json()]
            for file_name in file_names:
                content_url = initial_route.replace('https://github.com', 'https://raw.githubusercontent.com').replace('/tree-commit-info/','/')+'/'+file_name
                self.crawl_helper(content_url, option)
        else:
            response = CrawlerService.get_page_content(f"{initial_route}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
            data.extend(self.parse_page(response.text, initial_route,  option))
          
        self.update(option, data)
        
    def parse_page(self, response, url,  crawler_option):
        data = []
        data.extend(response.strip().split('\n'))
        return data