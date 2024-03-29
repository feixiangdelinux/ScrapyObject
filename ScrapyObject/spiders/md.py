# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
发布地址http://www.x95.cc/
scrapy crawl md -o md.json
https://5151md.me/

https://66sex.tv/
http://chujia.cc/
https://mogu.club/
https://59z.cc/
'''


class MdSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '5151md'
    # 后缀
    suffix = '.me/'
    name = 'md'
    allowed_domains = [website + '.me']
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
