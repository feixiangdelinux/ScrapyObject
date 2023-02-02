# -*- coding: utf-8 -*-

from ScrapyObject.spiders.utils.url_utils import *

'''
scrapy crawl hbsy -o hbsy.json
星期四 上午 11:17
'''
class HbsySpider(scrapy.Spider):
    name = 'hbsy'
    allowed_domains = ['www.yeyehai30.vip']
    start_urls = ['http://www.yeyehai30.vip/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        tags = response.xpath("//h3[@class='title']/text()").extract()
        v_url_list = get_video_url_one(content)
        if len(v_url_list):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=v_url_list[0])
        elif len(tags) == 1:
            url_list = response.xpath("//a[@class='myui-vodlist__thumb lazyload']/@ href").extract()
            name_list = response.xpath("//a[@class='myui-vodlist__thumb lazyload']/@ title").extract()
            pic_list = response.xpath("//a[@class='myui-vodlist__thumb lazyload']/@ data-original").extract()
            for index, value in enumerate(url_list):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0].strip(), url=split_joint('http://www.yeyehai30.vip/', value), name=name_list[index], pUrl=pic_list[index])
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint('http://www.yeyehai30.vip/', url), callback=self.parse)
