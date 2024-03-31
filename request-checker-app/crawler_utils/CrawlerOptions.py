from enum import Enum
class CrawlerOptions(Enum):
    XSS = 1
    SSTI = 2
    SQLI = 3
    XEE = 4
    XSLT = 5
    WS = 6
    NOSQLI = 7
    LFI = 8
    PP = 9
    CMDI = 10
    