# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://www.aishi5.com/
# 创建爬虫
# scrapy genspider aishi www.aishi5.com
# 运行爬虫ok
# scrapy crawl aishi -o aishi.json
class AishiSpider(scrapy.Spider):
    name = 'aishi'
    website = 'aishi5'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.aishi5.com/']
    start_urls = ['http://www.aishi5.com/index.php/vod/play/id/241989/sid/2/nid/1.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'https:.*?\.M3U8', content, re.IGNORECASE)
        print('aaaaaaaaaaaaa')
        print(video_url)
