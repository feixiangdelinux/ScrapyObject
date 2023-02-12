# -*- coding: utf-8 -*-
from urllib import request
from ScrapyObject.spiders.utils.url_utils import *

'''
scrapy crawl rottweilerchat -o rottweilerchat.json
http://rottweilerchat.com
'''


class RottweilerchatSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://'
    # 中缀
    website = 'rottweilerchat'
    # 后缀
    suffix = '.com/'
    name = 'rottweilerchat'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        aa = re.findall(r'video:(?:.|\n)*?}', content, re.IGNORECASE)
        if len(aa):
            bb = re.findall(r'http.*?\'', aa[0], re.IGNORECASE)
            print(aa)
            print(bb)
            name = response.xpath('/html/head/title/text()').extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='热播', url='', name=name[0], pUrl=bb[-1][:-1], vUrl=bb[0][:-1])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
