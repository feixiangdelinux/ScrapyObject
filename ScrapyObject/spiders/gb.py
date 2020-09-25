# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://5g34b.com/h/67672/
# 创建爬虫
# scrapy genspider gb 5g34b.com
# 运行爬虫
# scrapy crawl gb -o gb.json
class GbSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '5g34b'
    # 后缀
    suffix = '.com/'
    name = 'gb'
    allowed_domains = ['5g34b.com']
    start_urls = ['http://5g34b.com/']

    # start_urls = ['https://5g34b.com/h/60426/']
    # start_urls = ['https://5g34b.com/h/51860/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = response.xpath("//span[@id='downloadurl']/text()").extract()
        pic_url = response.xpath("//span[@id='purl']/text()").extract()
        if len(video_url) and len(pic_url):
            name = response.xpath("//div[@class='b_t']/text()").extract()
            tags = response.xpath("//li[@class='on']//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[0],
                                 purl=split_joint(self.prefix + self.website + self.suffix, pic_url[0]),
                                 vurl='https://5g717g.com/mp4/' + video_url[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.endswith('/') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
