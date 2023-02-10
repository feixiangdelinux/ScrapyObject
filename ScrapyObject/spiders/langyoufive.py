import scrapy


class LangyoufiveSpider(scrapy.Spider):
    name = 'langyoufive'
    allowed_domains = ['6691av.com']
    start_urls = ['http://6691av.com/']

    def parse(self, response):
        pass
