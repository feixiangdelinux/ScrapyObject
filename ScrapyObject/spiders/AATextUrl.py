# -*- coding: utf-8 -*-
import json

import scrapy

from ScrapyObject.items import VideoBean, VideoInfo
# 创建爬虫
# scrapy genspider rottweilerchat https://rottweilerchat.com
"""
https://d2xb.com
https://acbcn.com
https://abpg.net
https://aicespade23.top

"""
class AcbTextSpider(scrapy.Spider):
    name = 'acbText'
    # scrapy crawl acbText -o aqdavText.json
    file_name = 'aqdav1'
    # scrapy crawl acbText -o aqdtvText.json
    # file_name = 'aqdtv1'
    # scrapy crawl acbText -o ckText.json
    # file_name = 'ck1'
    # scrapy crawl acbText -o buzzText.json
    # file_name = 'buzz1'
    # scrapy crawl acbText -o seText.json
    # file_name = 'se1'
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
