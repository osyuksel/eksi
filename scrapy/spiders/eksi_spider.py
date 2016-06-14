import scrapy
from scrapy import optional_features
optional_features.remove('boto')

from eksisozluk.items import EksiSozlukEntry

from bs4 import BeautifulSoup

class EksiSpider(scrapy.Spider):
    name = "eksi"
    allowed_domains = ["eksisozluk.com"]
    start_urls = ["https://eksisozluk.com/eksi-itiraf--1037199?p=1"]
    current_page = 1
    entry_count = 0
    max_page_count = None
    download_delay = 1.5
    
    def parse(self, response):
    
        #If page count is unknown, fill it in
        if self.max_page_count is None:
            self.max_page_count = int(response.xpath("//div[@class=\'pager\']//@data-pagecount")[0].extract())

    
        #Write entire file in case I want to work offline
        filename = "eksi_itiraf_" + str(self.current_page) + ".html"
        with open("data//raw//" + filename, 'wb') as f:
            f.write(response.body)
     
        #Get all containers that contain an entry 
        #response.xpath('//li[@data-author]//div[@class=\'content\']')        
            containers = response.xpath('//li[@data-author]')        
        
        for cont in containers:
            #Get text
            text_raw = cont.xpath('.//div[@class=\'content\']').extract()[0]
            soup = BeautifulSoup(text_raw, 'html.parser')
            text = soup.get_text()
            
         
            #Author
            author = cont.xpath('.//div[@class=\'info\']//a[@class=\'entry-author\']//text()').extract()[0]
            
            
            #ID
            url = cont.xpath('.//div[@class=\'info\']//a[@class=\'entry-date permalink\']//@href').extract()[0]
            id = url.split('/')[-1]
            
            entry_no = self.entry_count        
            self.entry_count += 1
            
            page_no = self.current_page
            
            
            #Object to yield
            entry = EksiSozlukEntry()        
            entry['text'] = text
            entry['author'] = author
            entry['id'] = id
            entry['entry_no'] = entry_no
            entry['page_no'] = page_no
            
            yield entry
        
        
        #Go to next page
        self.current_page += 1

        if self.current_page > self.max_page_count:
            return

        next_page = "https://eksisozluk.com/eksi-itiraf--1037199?p=%d" % self.current_page
        yield scrapy.Request(next_page, self.parse)