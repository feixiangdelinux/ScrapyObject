# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://ddxx88.com/htm/mv9/73589.htm
# 创建爬虫
# scrapy genspider ddxx ddxx88.com
# 运行爬虫
class DdxxSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://'
    # 中缀
    website = 'ddxx88'
    # 后缀
    suffix = '.com/'
    name = 'ddxx'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]
    # start_urls = ['http://ddxx88.com/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url_one = response.xpath(
            "//div[@class='col-md-9 col-sm-12 col-xs-12 player_left max']//script//text()").extract()
        if len(video_url_one) and 'var src =' in video_url_one[0]:
            video_url = get_video_url_one(video_url_one[-1])
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vurl=video_url[0].replace("\\/", "/"))
        # 整理图片数据
        pic_url = response.xpath("//div[@class='col-md-9']//img/@ src").extract()
        if len(pic_url):
            url = response.xpath("//div[@class='play-list']//a/@ href").extract()
            name = response.xpath("//div[@class='player_title']//h1/text()").extract()
            tags = response.xpath("//div[@class='player_title']//div//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0],
                                 url=split_joint(self.prefix + self.website + self.suffix, url[0]), tags=tags[-1],
                                 purl=split_joint(self.prefix + self.website + self.suffix, pic_url[0]))
        # 提取url
        for url in url_list:
            if url.endswith('.htm') and url.startswith('/'):
                full_url = split_joint(self.prefix + self.website + self.suffix, url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
