# -*- coding: utf-8 -*-
import json

import scrapy

from ScrapyObject.items import VideoBean, VideoInfo


# 运行爬虫
# scrapy crawl oumeidText -o oumeidText.json
class IzhrbSpider(scrapy.Spider):
    name = 'oumeidText'

    def start_requests(self):
        f = open(r"/home/ccg/oumeid.json", "r", encoding='UTF-8')  # 设置文件对象
        str = f.read()  # 将txt文件的所有内容读入到字符串str中
        f.close()  # 将文件关闭
        inp_dict = json.loads(str, object_hook=VideoBean)
        for i in inp_dict:
            yield scrapy.Request(i['vUrl'], method='HEAD')

    def __init__(self):
        self.i = 1

    def parse(self, response):
        if 200 == response.status:
            lens = int.from_bytes(response.headers['Content-Length'], byteorder='big', signed=False)
            if lens != 0:
                item = VideoInfo()
                item['id'] = self.i
                item['status'] = 1
                if response.meta.get('redirect_urls') is None:
                    item['vUrl'] = response.url
                else:
                    item['vUrl'] = response.meta.get('redirect_urls')[0]
                self.i = self.i + 1
                yield item
