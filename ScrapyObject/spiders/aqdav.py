# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl aqdav -o aqdav.json
https://ugzaawjque.sbs/
'''


class AqdavSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'ugzaawjque'
    # 后缀
    suffix = '.sbs/'
    name = 'aqdav'
    allowed_domains = [website + '.sbs']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        pUrls = re.findall(r'thumbnailUrl.*?",', content, re.IGNORECASE)
        str_re1 = response.xpath("//span[@aria-current='page']//a/@ title").extract()
        if len(video_url) and len(pUrls) and len(str_re1):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=str_re1[0], url="", name=str_re1[-1][:-3], pUrl=pUrls[0][16:-2], vUrl=video_url[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
