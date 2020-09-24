# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://mm66p.com/
# 创建爬虫
# scrapy genspider mmp mm66p.com
# 运行爬虫
# scrapy crawl mmp -o mmp.json
class MmpSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'mm66p'
    # 后缀
    suffix = '.com/'
    name = 'mmp'
    allowed_domains = ['mm66p.com']
    start_urls = ['https://mm66p.com/']

    # start_urls = ['https://mm66p.com/suoyoushipin/dongman/23986.html']
    # start_urls = ['https://mm66p.com/suoyoushipin/dongman/']

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
            for k in video_url:
                self.i = self.i + 1
                yield get_video_item(id=self.i, url=response.url, vurl=k)
        # 整理图片数据
        name = response.xpath("//div[@class='pos']//a/@ title").extract()
        url = response.xpath("//div[@class='pos']//a/@ href").extract()
        pic_url = response.xpath("//div[@class='pos']//a//img/@ src").extract()
        if len(name) and len(pic_url):
            tags = response.xpath("//div[@class='tit']/text()").extract()
            ta = tags[0][tags[0].rfind(' > ') + 3:-2]
            for k in name:
                position = name.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=k,
                                     url=split_joint(self.prefix + self.website + self.suffix, url[position]),
                                     tags=ta, purl=pic_url[position])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint(self.prefix + self.website + self.suffix, url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)