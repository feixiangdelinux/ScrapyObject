# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已失效
scrapy crawl se -o se.json
http://yu293.com/
'''


class SeSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://'
    # 中缀
    website = 'yu293'
    # 后缀
    suffix = '.com/'
    name = 'se'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=format_url_one(video_url[0]))
        urls = response.xpath("//div[@class='detail-poster']//a/@href").extract()
        pUrls = response.xpath("//div[@class='detail-poster']//a//img/@src").extract()
        names = response.xpath("//div[@class='detail-poster']//a//img/@alt").extract()
        tags = response.xpath("//div[@class='breadcrumbs']//a/text()").extract()
        if len(urls) and len(names) and len(pUrls) and len(tags):
            for i in range(len(urls)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[-1], url=split_joint(self.prefix + self.website + self.suffix, urls[0]), name=names[0], pUrl=pUrls[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
