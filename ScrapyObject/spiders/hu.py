# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://www.369hu.com/vod/katongdongman/
# 创建爬虫
# scrapy genspider hu www.369hu.com
# 运行爬虫
# scrapy crawl hu -o hu.json
class HuSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '369hu'
    # 后缀
    suffix = '.com/'
    name = 'hu'
    allowed_domains = ['www.' + website + '.com']
    start_urls = [prefix + website + suffix]
    # start_urls = ['http://www.369hu.com/']

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
            yield get_video_item(id=self.i, url=response.url, vurl=format_url_one(video_url[-1]))
        # 整理图片数据
        name = response.xpath("//div[@id='tpl-img-content']//li//a/@ title").extract()
        tags = response.xpath("//a[@href='javascript:;']/text()").extract()
        if len(name) and len(tags):
            url = response.xpath("//div[@id='tpl-img-content']//li//a/@ href").extract()
            pic_url = response.xpath("//div[@id='tpl-img-content']//li//a//img/@ data-original").extract()
            for k in name:
                position = name.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=k,
                                     url=split_joint(self.prefix + self.website + self.suffix, url[position]),
                                     tags=tags[0], purl=pic_url[position])
        # 提取url
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and '\'' not in url and 'javascript' not in url and '#' not in url:
                if url.startswith('/'):
                    yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)
