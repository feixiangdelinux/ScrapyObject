# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *

# 创建爬虫
# scrapy genspider msp www.7msp8.com
# 运行爬虫
# sudo scrapy crawl msp -o msp.json
class MspSpider(scrapy.Spider):
    website = '7msp8'
    name = 'msp'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/']
    def parse(self, response):
        content = get_data(response)
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            # full_url = split_joint('https://www.' + self.website + '.com/', url)
            print(url)
            # yield scrapy.Request(full_url, callback=self.parse)
