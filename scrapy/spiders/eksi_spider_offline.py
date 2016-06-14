import scrapy
from scrapy import optional_features
optional_features.remove('boto')

from eksisozluk.items import EksiSozlukEntry

from bs4 import BeautifulSoup

#List files in the directory
import os

from lxml import html

class EksiSozlukOfflineSpider
    def __init__(self):
        self.entry_count = 0

    def start_crawl(self):
        page_list = os.listdir('../eksisozluk/data/raw')
        page_list = sorted(page_list, key=lambda k: int(k.split('_')[-1])  )

        print page_list

        entry_list = []
        for page_no, filename in enumerate(page_list):
            for entry in self.parse(filename, page_no):
                entry_list.append(entry)





    def parse(self, page_path, page_no):
        #Get all containers that contain an entry
        #response.xpath('//li[@data-author]//div[@class=\'content\']')

        page_fh = open(page_path, 'r')
        content = page_fh.read()
        page_fh.close()

        tree = html.fromstring(content)

        containers = tree.xpath('//li[@data-author]')

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
            entry = {}
            entry['text'] = text
            entry['author'] = author
            entry['id'] = id
            entry['entry_no'] = entry_no
            entry['page_no'] = page_no

            yield entry
