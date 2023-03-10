# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl aqdav -o aqdav.json
https://vip.aqdz110.com
'''


class AqdavSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://vip.'
    # 中缀
    website = 'aqdz110'
    # 后缀
    suffix = '.com/'
    name = 'aqdav'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        aa = re.findall(r'video:(?:.|\n)*?}', content, re.IGNORECASE)
        if len(aa):
            name = response.xpath("//ol[@class='breadcrumb']//li/text()").extract()
            tags = response.xpath("//ol[@class='breadcrumb']//li//a/text()").extract()
            bb = re.findall(r'http.*?\'', aa[0], re.IGNORECASE)
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[-1], url='', name=name[0], pUrl=bb[-1][:-1], vUrl=bb[0][:-1])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
