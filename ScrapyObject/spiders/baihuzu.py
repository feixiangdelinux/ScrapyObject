# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.baihuzu.cyou/index.php/vod/play/id/86521/sid/1/nid/1.html
# 创建爬虫
# scrapy genspider baihuzu www.baihuzu.cyou
# 运行爬虫
# scrapy crawl baihuzu -o baihuzu.json
class BaihuzuSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'baihuzu'
    # 后缀
    suffix = '.cyou/'
    name = 'baihuzu'
    allowed_domains = ['www.' + website + '.cyou']
    start_urls = [prefix + website + suffix]
    # start_urls = ['https://www.baihuzu.cyou/']

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
            yield get_video_item(id=self.i, url=response.url, vurl=format_url_one(video_url[0]))
        # 整理图片数据
        name = response.xpath("//div[@class='pic']//ul//a/@ title").extract()
        tags = response.xpath("//div[@class='title']//li//a/text()").extract()
        if len(name) and len(tags):
            url = response.xpath("//div[@class='pic']//ul//a/@ href").extract()
            pic_url = response.xpath("//div[@class='pic']//ul//a//img/@ src").extract()
            for k in name:
                position = name.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=k,
                                     url=split_joint(self.prefix + self.website + self.suffix, url[position]),
                                     tags=tags[0], purl=pic_url[position])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
