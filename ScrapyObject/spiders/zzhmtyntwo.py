# -*- coding: utf-8 -*-
import json

import scrapy

from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import get_data


# scrapy genspider zzhmtyntwo zzhmtyntwo.com
# 运行爬虫
# scrapy crawl zzhmtyntwo -o zzhmtyntwo.json
class ZzhmtyntwoSpider(scrapy.Spider):
    name = 'zzhmtyntwo'
    website = 'zzhmtyn188'
    allowed_domains = [website + '.com']

    def start_requests(self):
        f = open(r"/home/ccg/zzhmtyn.json", "r", encoding='UTF-8')  # 设置文件对象
        str = f.read()  # 将txt文件的所有内容读入到字符串str中
        f.close()  # 将文件关闭
        inp_dict = json.loads(str, object_hook=VideoBean)
        for i in inp_dict:
            if i['vUrl'].strip() != '':
                yield scrapy.Request(i['vUrl'], method='HEAD')

    def __init__(self):
        self.i = 1

    def parse(self, response):
        # content = get_data(response)
        print('250:aaaaaaaaaa')
        print(response.headers)
        print(response.text)
        print('250:bbbbbbbbbbbb')
