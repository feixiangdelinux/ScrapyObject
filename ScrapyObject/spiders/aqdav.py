# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
未完成
scrapy crawl aqdav -o aqdav.json
https://66.td-seo-0-26.top/
'''


class AqdavSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://66.'
    # 中缀
    website = 'td-seo-0-26'
    # 后缀
    suffix = '.top/'
    name = 'aqdav'
    allowed_domains = [website + '.top']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        tags = response.xpath("/html/head/meta[@name='keywords']/@ content").extract()[0]
        pUrls = response.xpath("//div[@class='detail-poster']//a//img/@ src").extract()
        names = response.xpath("//div[@class='detail-poster']//a//img/@ alt").extract()
        urls = response.xpath("//div[@class='detail-poster']//a/@ href").extract()
        if len(pUrls) and len(names) and len(urls):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[:tags.find(names[0])], url=split_joint(self.prefix + self.website + self.suffix, urls[0]), name=names[0], pUrl=pUrls[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
