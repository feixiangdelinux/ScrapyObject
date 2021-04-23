# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider fqypzxxx www.fqypzxxx.com
# 运行爬虫ok
# scrapy crawl fqypzxxx -o fqypzxxx.json
class FqypzxxxSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'fqypzxxx'
    # 后缀
    suffix = '.com/'
    name = 'fqypzxxx'
    allowed_domains = ['www.' + website + '.com']
    start_urls = [prefix + website + suffix]

    # start_urls = ['http://www.fqypzxxx.com/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        if len(video_url) and '"' not in video_url[0]:
            self.i = self.i + 1
            yield get_video_item(id=self.i, vurl=format_url_one(video_url[0]))
        # 整理图片数据
        pic_url = response.xpath("//div[@class='film_info clearfix']//img/@ src").extract()
        if len(pic_url):
            tags = response.xpath("//div[@class='box cat_pos clearfix']//a/text()").extract()
            url = response.xpath("//div[@class='film_bar clearfix']//a/@ href").extract()
            name = response.xpath("//dd[@class='film_title']/text()").extract()
            for k in url:
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[0].strip(),tags=tags[-1],purl=pic_url[0])
        # 提取url
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and 'www.' not in url and 'javascript' not in url:
                if url.startswith('/'):
                    yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url),callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)
