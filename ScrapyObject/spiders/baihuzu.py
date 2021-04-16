# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://igv.baihuzu.buzz/
# 创建爬虫
# scrapy genspider baihuzu igv.baihuzu.buzz
# 运行爬虫
# scrapy crawl baihuzu -o baihuzu.json
class BaihuzuSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://igv.'
    # 中缀
    website = 'baihuzu'
    # 后缀
    suffix = '.buzz/'
    name = 'baihuzu'
    allowed_domains = ['igv.' + website + '.buzz']
    start_urls = [prefix + website + suffix]
    # start_urls = ['https://igv.baihuzu.buzz/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)

        # # 整理视频数据
        # video_url = get_video_url_one(content)
        # if len(video_url):
        #     self.i = self.i + 1
        #     yield get_video_item(id=self.i, url=response.url, vurl=format_url_one(video_url[0]))
        # # 整理图片数据
        # name = response.xpath("//div[@class='pic']//ul//a/@ title").extract()
        # tags = response.xpath("//div[@class='title']//li//a/text()").extract()
        # if len(name) and len(tags):
        #     url = response.xpath("//div[@class='pic']//ul//a/@ href").extract()
        #     pic_url = response.xpath("//div[@class='pic']//ul//a//img/@ src").extract()
        #     for k in name:
        #         position = name.index(k)
        #         self.i = self.i + 1
        #         yield get_video_item(id=self.i, name=k,tags=tags[0], purl=pic_url[position])
        # # 提取url
        for url in url_list:
            print(url)
            # if url.endswith('.html') and url.startswith('/'):
            #     yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            # elif url.startswith('http') or url.startswith('igv'):
            #     yield scrapy.Request(url, callback=self.parse)
