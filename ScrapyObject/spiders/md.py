# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
发布地址http://www.7000.me/
scrapy crawl md -o md.json
http://53894.com/
'''


class MdSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '53894'
    # 后缀
    suffix = '.com/'
    name = 'md'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        else:
            url = response.xpath("//p[@class='img']//a/@ href").extract()
            name = response.xpath("//p[@class='img']//img/@ title").extract()
            p_url = response.xpath("//p[@class='img']//img/@ src").extract()
            tag = response.xpath("//span[@class='detail_right_span']/text()").extract()
            if len(p_url) == len(name) and len(p_url) == len(url) and len(tag):
                for index, value in enumerate(p_url):
                    self.i = self.i + 1
                    yield get_video_item(id=self.i, tags=tag[0], url=split_joint(self.prefix + self.website + self.suffix, url[index]), name=name[index], pUrl=p_url[index], vUrl='')
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
