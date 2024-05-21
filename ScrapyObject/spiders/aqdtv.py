# -*- coding: utf-8 -*-
import urllib.parse

from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl aqdtv -o aqdtv.json
http://www.8655z.com/
'''


class AqdtvSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '8655z'
    # 后缀
    suffix = '.com/'
    name = 'aqdtv'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=urllib.parse.unquote(format_url_one(video_url[0])))
        name_list = response.xpath("//div[@class='player']//div[@class='a11']/text()").extract()
        url_list = response.xpath("//div[@class='playurl']//ul//a/@ href").extract()
        img_list = response.xpath("//div[@class='player']//div//table//tr//td//div//img/@ src").extract()
        if len(name_list) and len(url_list) and len(img_list):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags="综合", url=split_joint(self.prefix + self.website + self.suffix, url_list[0]), name=name_list[0], pUrl=img_list[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
