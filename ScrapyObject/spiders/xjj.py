# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://www.86xjj.com/html/vod/52642.html
# 创建爬虫
# scrapy genspider xjj www.86xjj.com
# 运行爬虫
# scrapy crawl xjj -o xjj.json
class XjjSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '86xjj'
    # 后缀
    suffix = '.com/'
    name = 'xjj'
    allowed_domains = ['www.86xjj.com']
    start_urls = ['http://www.86xjj.com/']

    # start_urls = ['http://www.86xjj.com/html/vod/52642.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        # 整理视频数据
        pic_url = response.xpath("//ul[@class='img']//img/@ src").extract()
        name = response.xpath("//span[@class='btns']/text()").extract()
        if len(video_url) and len(pic_url):
            l2 = list(set(video_url))
            for k in l2:
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[0], url=response.url, tags=name[1], purl=pic_url[0], vurl=k)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint(self.prefix + self.website + self.suffix, url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
