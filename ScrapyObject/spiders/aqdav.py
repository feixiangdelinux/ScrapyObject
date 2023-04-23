# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl aqdav -o aqdav.json
https://vip.aqdw82.com/
'''

class AqdavSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://vip.'
    # 中缀
    website = 'aqdw82'
    # 后缀
    suffix = '.com/'
    name = 'aqdav'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        name = response.xpath("//script/text()").extract()
        for url in name:
            if ".m3u8" in url:
                p_url = re.findall(r'http.*?\.jpg', url, re.IGNORECASE)
                video_url = get_video_url_one(url)
                name = response.xpath("//ol[@class='breadcrumb']//li/text()").extract()
                tags = response.xpath("//ol[@class='breadcrumb']//li//a/text()").extract()
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[-1], url='', name=name[0], pUrl=p_url[0], vUrl=video_url[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
