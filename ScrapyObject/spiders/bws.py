# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.bws6.com/
# 创建爬虫
# scrapy genspider bws www.bws6.com
# 运行爬虫
# scrapy crawl bws -o bws.json
class BwsSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'bwj7'
    # 后缀
    suffix = '.com/'
    name = 'bws'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/index/home.html']

    # start_urls = ['https://www.bwj7.com/index/home.html']
    # start_urls = ['https://www.bwj7.com/shipin/list-%E4%BA%9A%E6%B4%B2%E7%94%B5%E5%BD%B1-2.html']
    # start_urls = ['https://www.bwj7.com/shipin/91782.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        tags = response.xpath(
            "//div[@class='pull-left text-left margin_left_10 pull-left-mobile2']//div//p/text()").extract()
        if len(video_url) and len(tags):
            name = response.xpath('/html/head/title/text()').extract()
            pic_url = response.xpath("//div[@class='pull-left pull-left-mobile1']//div//img/@ data-original").extract()
            l2 = list(set(video_url))
            for k in l2:
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[0].strip(), url=response.url, tags=tags[0][3:],
                                     purl=pic_url[0], vurl=k)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
