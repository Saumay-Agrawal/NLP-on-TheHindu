import scrapy
from pymongo import MongoClient
import json

client = MongoClient()
db = client['TheHindu']
col = db['test-data']


class TheHinduSpider(scrapy.Spider):

    name = "TheHinduSpider"
    allowed_domains = "www.thehindu.com"
    start_urls = ("https://www.thehindu.com/",)

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        for link in links:
            if('www.thehindu.com' in link):
                link = link.split('?')[0]
                # print(link)
                if(link[-4:]=='.ece'):
                    yield scrapy.Request(url=link, callback=self.parse_article)
                else:
                    yield scrapy.Request(url=link, callback=self.parse)
    
    def parse_article(self, response):
        self.log(response.url)
        data = {}
        data['link'] = response.url
        col.insert(data)