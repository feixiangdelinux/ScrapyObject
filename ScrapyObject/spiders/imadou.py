# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
需要翻墙
scrapy crawl imadou -o imadou.json
https://www.mogu.club/
'''


class ImadouSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'mogu'
    # 后缀
    suffix = '.club/'
    name = 'imadou'
    allowed_domains = [website + '.club']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        url = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ href").extract()
        name = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ title").extract()
        p_url = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ data-original").extract()
        tag = response.xpath("//div[@class='stui-pannel clearfix']//div[@class='stui-pannel__head clearfix']//h3[@class='title']/text()").extract()
        if len(p_url) == len(name) and len(p_url) == len(url) and len(tag) == 1:
            for index, value in enumerate(p_url):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tag[-1].strip(), url=split_joint(self.prefix + self.website + self.suffix, url[index]), name=name[index], pUrl=p_url[index], vUrl='')
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
