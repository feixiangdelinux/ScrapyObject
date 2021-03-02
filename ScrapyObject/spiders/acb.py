# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.59ac3eebf2f7.com/index/home.html
# 创建爬虫
# scrapy genspider acb www.acb9276ce215.com
# 运行爬虫
# scrapy crawl acb -o acb.json
# https://bkimg.cdn.bcebos.com/pic/3bf33a87e950352a87460b265043fbf2b2118bfc?x-bce-process=image/watermark,image_d2F0ZXIvYmFpa2U5Mg==,g_7,xp_5,yp_5
class AcbSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '59ac3eebf2f7'
    # 后缀
    suffix = '.com/'
    name = 'acb'
    allowed_domains = ['www.' + website + '.com']
    start_urls = [prefix + website + '.com/index/home.html']

    # start_urls = ['https://www.59ac3eebf2f7.com/index/home.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        video_url = response.xpath("//script/text()").extract()
        name = response.xpath("//meta[@name='keywords']/@ content").extract()
        tags = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
        # 整理视频数据
        video_url_one = get_video_url_one(content)
        if len(video_url_one) and len(name) and len(tags):
            final_video_url = list(set(video_url_one))
            self.i = self.i + 1
            for k in final_video_url:
                yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1], purl='', vurl=k)
        if len(video_url):
            if 'var video' in video_url[0]:
                pattern = re.compile("'(.*)'")
                str_re1 = pattern.findall(video_url[0])
                if str_re1[0].startswith('/'):
                    if 'https://' in str_re1[1]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1], purl='',
                                             vurl=str_re1[1] + str_re1[0])
                    if 'https://' in str_re1[2]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1], purl='',
                                             vurl=str_re1[2] + str_re1[0])
                    if 'https://' in str_re1[3]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1], purl='',
                                             vurl=str_re1[3] + str_re1[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
