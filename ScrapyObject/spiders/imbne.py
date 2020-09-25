# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://www.imbne.com/
# 创建爬虫
# scrapy genspider imbne www.imbne.com
# 运行爬虫
# scrapy crawl imbne -o imbne.json
class ImbneSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'imbne'
    # 后缀
    suffix = '.com/'
    name = 'imbne'
    allowed_domains = ['www.imbne.com']
    start_urls = ['http://www.imbne.com/']
    # start_urls = ['http://www.imbne.com/?m=vod-play-id-46970-src-1-num-1.html']
    # start_urls = ['http://www.imbne.com/?m=vod-detail-id-46970.html']

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
            yield get_video_item(id=self.i, url=response.url, vurl=format_url_two(video_url[0]))
        pic_url = response.xpath("//dl//dt//img/@ src").extract()
        name = response.xpath("//dl//dt//img/@ title").extract()
        tags = response.xpath("//dl//dd//span/text()").extract()
        url = response.xpath("//div[@class='film_bar clearfix']//ul//li//a/@ href").extract()
        if len(pic_url) and len(name) and len(tags) and len(url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0],
                                 url=split_joint(self.prefix + self.website + self.suffix, url[0]), tags=tags[0],
                                 purl=split_joint(self.prefix + self.website + self.suffix, pic_url[0]))
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
