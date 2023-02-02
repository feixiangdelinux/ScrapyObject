# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 运行爬虫ok
# scrapy crawl buzz -o buzz.json
class BuzzSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'xjjcaiji'
    # 后缀
    suffix = '.com/'
    name = 'buzz'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.xjjcaiji.com/home/index.html']

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
            tags = response.xpath("//span[@class='btns']/text()").extract()
            p_url = ''
            if 'https://xjjjt.hmpicimage.com/' in tags[2]:
                p_url = tags[2]
            else:
                p_url = split_joint(self.prefix + self.website + self.suffix, tags[2])
            print('https://xjjjt.hmpicimage.com/' in tags[2])
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[1], url="", name=tags[0], pUrl=p_url, vUrl=video_url[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
