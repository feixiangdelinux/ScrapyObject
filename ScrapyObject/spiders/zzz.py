from ScrapyObject.spiders.utils.url_utils import *

''''
测试
scrapy crawl zzz
https://www.cdnbus.help/forum
'''


class ZzzSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'cdnbus'
    # 后缀
    suffix = '.help/'
    name = 'zzz'
    allowed_domains = [website + '.help']
    start_urls = [prefix + website + suffix + 'forum']

    # start_urls = ["https://www.cdnbus.help/forum/"]
    start_urls = ["http://121.4.179.184:8800/game/index.html"]

    def parse(self, response):
        content = get_data(response)
        print(content)

            # if url.startswith('/') and url.endswith('.html'):
            #     yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)