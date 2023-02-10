import scrapy


class LangyousevenSpider(scrapy.Spider):
    name = 'langyouseven'
    allowed_domains = ['6613dy.com']
    start_urls = ['http://6613dy.com/']

    def parse(self, response):
        pass
