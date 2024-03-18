# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
scrapy crawl hsex -o hsex.json
http://www.743hh8.cfd/AAyidong/index.html
'''


class HsexSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '743hh8'
    # 后缀
    suffix = '.cfd/'
    name = "hsex"
    allowed_domains = [website + '.cfd']
    start_urls = [prefix + website + suffix + 'AAyidong/index.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        pUrls = response.xpath("//div[@class='thum']//div/@ style").extract()
        urls = response.xpath("//div[@class='thum']//div//a/@ href").extract()
        names = response.xpath("//div[@class='thum']//div//a//b/text()").extract()
        tags = response.xpath("//h2[@class='location']/text()").extract()
        if len(urls) and len(pUrls) and len(names) and len(tags):
            for i in range(len(pUrls)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0], url=split_joint(self.prefix + self.website + self.suffix, urls[i]), name=names[i], pUrl=pUrls[i][pUrls[i].find('(') + 1: pUrls[i].find(')')].strip())
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
