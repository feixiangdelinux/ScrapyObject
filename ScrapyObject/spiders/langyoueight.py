import scrapy


class LangyoueightSpider(scrapy.Spider):
    name = 'langyoueight'
    allowed_domains = ['7333dy.com']
    start_urls = ['http://7333dy.com/']

    def parse(self, response):
        pass
