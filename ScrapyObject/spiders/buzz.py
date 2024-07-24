# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl buzz -o buzz.json
https://www.kss822.vip/
'''


class BuzzSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'kss822'
    # 后缀
    suffix = '.vip/'
    name = 'buzz'
    allowed_domains = ['www.' + website + '.vip']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = response.body.decode('utf-8')
        # 整理视频数据
        video_url = get_video_url_one(content)
        tag_list = response.xpath("//h1//a/text()").extract()
        if len(video_url) and len(tag_list):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tag_list[-1], url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        url_list = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ href").extract()
        title_list = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ title").extract()
        pic_list = response.xpath("//a[@class='stui-vodlist__thumb lazyload']/@ data-original").extract()
        if len(url_list) and len(title_list) and len(pic_list):
            for index, value in enumerate(url_list):
                self.i = self.i + 1
                yield get_video_item(id=self.i, url=split_joint(self.prefix + self.website + self.suffix, url_list[index]), name=title_list[index], pUrl=pic_list[index])
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
