import scrapy


class LangyousixSpider(scrapy.Spider):
    name = 'langyousix'
    allowed_domains = ['094dy.com']
    start_urls = ['http://094dy.com/']

    def parse(self, response):
        pass
