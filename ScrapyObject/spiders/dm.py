# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider dm www.dm528.com
# 运行爬虫
# scrapy crawl dm -o dm.json
class DmSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'dm528'
    # 后缀
    suffix = '.com/'
    name = 'dm'
    allowed_domains = ['www.' + website + '.com']
    start_urls = [prefix + website + suffix]

    # start_urls = ['http://www.dm528.com/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        if len(video_url) and '"' not in video_url[0]:
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vurl=video_url[0].replace("\\/", "/"))
        # 整理图片数据
        pUrl = response.xpath("//div[@class='thumbnail']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//div[@class='thumbnail']//a/@ href").extract()
            tags = response.xpath("//div[@class='latest_title']/text()").extract()
            name = response.xpath("//div[@class='thumbnail']//img/@ title").extract()
            for k in pUrl:
                position = pUrl.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[position].strip(),
                                     url=split_joint(self.prefix + self.website + self.suffix, urls[position]),
                                     tags=tags[0][2:],
                                     purl=pUrl[position])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)