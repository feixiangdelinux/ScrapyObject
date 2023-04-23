# -*- coding: utf-8 -*-
import json

import scrapy

from ScrapyObject.items import VideoBean, VideoInfo

"""
创建爬虫
scrapy genspider ya http://www.544ya.com
http://www.imadou.cc
"""


class AcbTextSpider(scrapy.Spider):
    name = 'acbText'
    # scrapy crawl acbText -o acbText.json
    file_name = 'acb1'

    # scrapy crawl acbText -o aicespadeText.json
    # file_name = 'aicespade1'

    # scrapy crawl acbText -o aqdavText.json
    # file_name = 'aqdav1'

    # scrapy crawl acbText -o aqdtvText.json
    # file_name = 'aqdtv1'

    # scrapy crawl acbText -o buzzText.json
    # file_name = 'buzz1'

    # scrapy crawl acbText -o ckText.json
    # file_name = 'ck1'

    # scrapy crawl acbText -o hbsyText.json
    # file_name = 'hbsy1'

    # scrapy crawl acbText -o hsexText.json
    # file_name = 'hsex1'

    # scrapy crawl acbText -o imadouText.json
    # file_name = 'imadou1'

    # scrapy crawl acbText -o langyouText.json
    # file_name = 'langyou1'

    # scrapy crawl acbText -o langyoueightText.json
    # file_name = 'langyoueight1'

    # scrapy crawl acbText -o langyoufiveText.json
    # file_name = 'langyoufive1'

    # scrapy crawl acbText -o langyoufourText.json
    # file_name = 'langyoufour1'

    # scrapy crawl acbText -o langyouoneText.json
    # file_name = 'langyouone1'

    # scrapy crawl acbText -o langyousevenText.json
    # file_name = 'langyouseven1'

    # scrapy crawl acbText -o langyousixText.json
    # file_name = 'langyousix1'

    # scrapy crawl acbText -o langyouthreeText.json
    # file_name = 'langyouthree1'

    # scrapy crawl acbText -o mdText.json
    # file_name = 'md1'

    # scrapy crawl acbText -o langyouoneText.json
    # file_name = 'langyouone1'

    # scrapy crawl acbText -o seText.json
    # file_name = 'se1'

    # scrapy crawl acbText -o xsmdlText.json
    # file_name = 'xsmdl1'

    # scrapy crawl acbText -o yaText.json
    # file_name = 'ya1'

    # scrapy crawl acbText -o yrefText.json
    # file_name = 'yref1'
    def start_requests(self):
        # f = open("/home/ccg/" + self.file_name + '.json', "r", encoding='UTF-8')  # 设置文件对象
        f = open('E:\\' + self.file_name + '.json', "r", encoding='UTF-8')  # 设置文件对象
        str = f.read()  # 将txt文件的所有内容读入到字符串str中
        f.close()  # 将文件关闭
        inp_dict = json.loads(str, object_hook=VideoBean)
        for i in inp_dict:
            yield scrapy.Request(i['vUrl'], method='HEAD')

    def __init__(self):
        self.i = 1

    def parse(self, response):
        if 200 == response.status:
            item = VideoInfo()
            item['id'] = self.i
            if response.meta.get('redirect_urls') is None:
                item['vUrl'] = response.url
            else:
                item['vUrl'] = response.meta.get('redirect_urls')[0]
            self.i = self.i + 1
            yield item
