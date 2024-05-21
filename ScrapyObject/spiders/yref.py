# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

''''
已失效
scrapy crawl yref -o yref.json
http://www.as84.com/
'''


class YrefSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'as84'
    # 后缀
    suffix = '.com/'
    name = 'yref'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl="", vUrl=video_url[0])
        tags = response.xpath("//div[@class='film_info clearfix']//dl//dd//span/text()").extract()
        url = response.xpath("//a[@title='在线播放']/@href").extract()
        p_url = response.xpath("//div[@class='film_info clearfix']//dl//dt//img/@src").extract()
        name = response.xpath("//div[@class='film_info clearfix']//dl//dt//img/@title").extract()
        if len(tags) and len(name) and len(p_url) and len(url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[0], url=self.prefix + self.website + '.com' + url[0], name=name[0], pUrl=p_url[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
