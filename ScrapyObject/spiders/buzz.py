# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider qp www.q22p.cc
# 运行爬虫ok
# scrapy crawl buzz -o buzz.json
# ok
class BuzzSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'hzz01zb9ov'
    # 后缀
    suffix = '.buzz/'
    name = 'buzz'
    allowed_domains = ['www.' + website + '.buzz']

    start_urls = [prefix + website + suffix]

    # start_urls = ['http://www.hzz01zb9ov.buzz/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            if response.url.endswith('/'):
                yield get_video_item(id=self.i, vurl=format_url_two(video_url[0]))
            else:
                yield get_video_item(id=self.i, vurl=format_url_two(video_url[0]))
        # 整理图片数据
        tags = response.xpath("//li[@class='n1']//b/text()").extract()
        name = response.xpath("//div[@class='post']//a/@ title").extract()
        url = response.xpath("//div[@class='post']//a/@ href").extract()
        pUrl = response.xpath("//div[@class='post']//a//img/@ src").extract()
        if len(pUrl):
            for k in pUrl:
                position = pUrl.index(k)
                self.i = self.i + 1
                if len(tags):
                    yield get_video_item(id=self.i, name=name[position], tags=tags[0], purl=pUrl[position])
                else:
                    yield get_video_item(id=self.i, name=name[position], tags='综合', purl=pUrl[position])

        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.endswith('/') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
