# -*- coding: utf-8 -*-

import base64

from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
scrapy crawl acb -o acb.json
https://www.4huub5.com/Enter/home.html
'''


class AcbSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '4huub5'
    # 后缀
    suffix = '.com/'
    name = 'acb'
    allowed_domains = ['www.' + website + '.com']
    start_urls = [prefix + website + suffix + 'Enter/home.html']
    def __init__(self):
        self.i = 0
    def parse(self, response):
        # 获取字符串类型的网页内容
        tag = ''
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            str_re1 = response.xpath('/html/head/title/text()').extract()
            tags = response.xpath("//div[@class='textlink']//a//script/text()").extract()
            tags_two = response.xpath("//div[@class='textlink']//a/text()").extract()
            if len(tags):
                if 'document.write(d(' in tags[-1]:
                    split1 = tags[-1].split("d('")
                    split2 = split1[1].split("'))")
                    if len(split2) > 0:
                        content = split2[0]
                    tag = base64.b64decode(content).decode("utf-8")
            elif len(tags_two):
                tag = tags_two[-1]
            for url_list in video_url:
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tag, url='', name=str_re1[0], pUrl='https://bkimg.cdn.bcebos.com/pic/3bf33a87e950352a87460b265043fbf2b2118bfc', vUrl=url_list)
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('/') and url.endswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
