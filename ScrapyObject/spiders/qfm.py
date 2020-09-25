# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://www.qfm12.me/index.php/vod/play/id/18422/sid/1/nid/1.html
# 创建爬虫
# scrapy genspider qfm www.qfm12.me
# 运行爬虫
# scrapy crawl qfm -o qfm.json
class QfmSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'qfm12'
    # 后缀
    suffix = '.me/'
    name = 'qfm'
    allowed_domains = ['www.qfm12.me']
    start_urls = ['http://www.qfm12.me/']
    # start_urls = ['http://www.qfm12.me/index.php/vod/play/id/18422/sid/1/nid/1.html']
    # start_urls = ['http://www.qfm12.me/index.php/vod/detail/id/18483.html']

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
        name = response.xpath("//h1[@class='fed-part-eone fed-font-xvi']//a/text()").extract()
        tags = response.xpath("//li[@class='fed-col-xs6 fed-col-md3 fed-part-eone']//a/text()").extract()
        pic_url = response.xpath("//a[@class='fed-list-pics fed-lazy fed-part-2by3']/@ style").extract()
        if len(name) and len(tags) and len(pic_url):
            url_one = response.xpath(
                "//a[@class='fed-btns-info fed-rims-info fed-part-eone fed-back-green']/@ href").extract()
            if len(url_one):
                aa = re.findall(r'[(](.*?)[)]', pic_url[0], re.IGNORECASE)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[0],
                                     url=split_joint(self.prefix + self.website + self.suffix, url_one[0]),
                                     tags=tags[0], purl=aa[0])
            url_two = response.xpath("//a[@class='fed-btns-info fed-rims-info fed-part-eone']/@ href").extract()
            if len(url_two):
                aa = re.findall(r'[(](.*?)[)]', pic_url[0], re.IGNORECASE)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[0],
                                     url=split_joint(self.prefix + self.website + self.suffix, url_two[0]),
                                     tags=tags[0], purl=aa[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint(self.prefix + self.website + self.suffix, url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)