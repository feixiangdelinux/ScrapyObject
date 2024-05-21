# -*- coding: utf-8 -*-
from html import unescape

from ScrapyObject.spiders.utils.url_utils import *
import base64

"""
已完成
scrapy crawl xyz -o xyz.json
https://www.999eei.com/
"""


class XyzSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '999eei'
    # 后缀
    suffix = '.com/'
    name = 'xyz'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'http.*?\.m3u8";', content, re.IGNORECASE)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl="", vUrl=video_url[0][:-2])
        tags = response.xpath("//div[@class='title']//h3//a/text()").extract()
        if len(tags):
            url = response.xpath("//div[@class='row col5 clearfix']//dl//dt//a/@ href").extract()
            name = response.xpath("//div[@class='row col5 clearfix']//dl//dt//a/@ title").extract()
            p_url = response.xpath("//div[@class='row col5 clearfix']//dl//dt//a//img/@ data-original").extract()
            for i in range(len(p_url)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0], url=split_joint(self.prefix + self.website + self.suffix, url[i]), name=name[i], pUrl=split_joint(self.prefix + self.website + self.suffix, p_url[i]), vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
