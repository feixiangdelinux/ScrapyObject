# -*- coding: utf-8 -*-

from ScrapyObject.spiders.utils.url_utils import *

'''
https://xsmdl.com
运行爬虫
scrapy crawl xsmdl -o xsmdl.json
'''


class XsmdlSpider(scrapy.Spider):
    name = 'xsmdl'
    allowed_domains = ['xsmdl.com']
    start_urls = ['https://xsmdl.com']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        v_url_list = get_video_url_one(content)
        if len(v_url_list):
            tags = response.xpath("//a[@class='genre']/text()").extract()
            str_re1 = response.xpath('/html/head/title/text()').extract()
            ind = str_re1[0].index('|')
            suffix_str = str_re1[0][3:ind]
            pUrl = response.xpath("//video[@id='player0']/@ data-poster").extract()
            for v_url in v_url_list:
                self.i = self.i + 1
                if v_url.find('.m3u8') != -1:
                    if len(tags):
                        ssss = tags[0].strip()
                    else:
                        ssss = "综合"
                    yield get_video_item(id=self.i, tags=ssss, url=response.url, name=suffix_str.strip(), pUrl=pUrl[0], vUrl=v_url)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('https'):
                yield scrapy.Request(url, callback=self.parse)
