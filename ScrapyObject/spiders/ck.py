# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl ck -o ck.json
https://o7p83hb2za2ko7wqu6o71fi7zaqq2k.zayy83.xyz/
'''


class CkSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://o7p83hb2za2ko7wqu6o71fi7zaqq2k.'
    # 中缀
    website = 'zayy83'
    # 后缀
    suffix = '.xyz/'
    name = 'ck'
    allowed_domains = [website + '.xyz']
    # start_urls = [prefix + website + suffix]
    start_urls = ['https://o7p83hb2za2ko7wqu6o71fi7zaqq2k.zayy83.xyz/gaoqingguochan/2.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = response.body.decode('utf-8', 'ignore')
        video_url = get_video_url_one(content)
        url_list = response.xpath("//div[@class='vod']//div[@class='vod-img']//a/@ href").extract()
        img_list = response.xpath("//div[@class='vod']//div[@class='vod-img']//a//img/@ data-original").extract()
        name_list = response.xpath("//div[@class='vod']//div[@class='vod-txt']//a/text()").extract()
        tags = response.xpath("//div[@class='title']//h3/text()").extract()
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=video_url[0])
        if len(url_list) and len(img_list) and len(name_list) and len(tags) == 2:
            for i in range(len(url_list)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0], url=split_joint(self.prefix + self.website + self.suffix, url_list[i]), name=name_list[i], pUrl=img_list[i], vUrl='')
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
