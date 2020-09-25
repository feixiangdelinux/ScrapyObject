# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://8x1048x.com/html/4655/
# 创建爬虫
# scrapy genspider xx 8x1048x.com
# 运行爬虫
# scrapy crawl xx -o xx.json
class XxSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '8x1048x'
    # 后缀
    suffix = '.com/'
    name = 'xx'
    allowed_domains = ['8x1048x.com']
    start_urls = ['https://8x1048x.com/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        pic_url = response.xpath("//span[@class='hiddenBox']/text()").extract()
        video_url = response.xpath("//div[@class='bf_an']//a/@ href").extract()
        if len(video_url) and len(pic_url):
            tags = response.xpath("//div[@class='dq_wz']//a/text()").extract()
            name = response.xpath("//div[@class='w_z']//h3/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1],
                                 purl=split_joint(self.prefix + self.website + self.suffix, pic_url[-1]),
                                 vurl=video_url[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint(self.prefix + self.website + self.suffix, url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
