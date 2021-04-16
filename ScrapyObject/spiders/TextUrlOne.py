# -*- coding: utf-8 -*-

import scrapy


# scrapy crawl acboneText
class AcbTextOneSpider(scrapy.Spider):
    name = 'acboneText'
    start_urls = ['']
    start_urls = ['https://s3.cdn-f8bef553ee8a3622.com/common/mm_m3u8_online/dm_MD6VHS33/hls/1/index.m3u8']

    # start_urls = ['https://s3.cdn-f8bef553ee8a3622.com/common/dm/2018_11/09/dm_rYTmLFn_wm/dm_rYTmLFn_wm.m3u8']

    def __init__(self):
        self.i = 1

    def parse(self, response):
        print(response.status)
        if 200 == response.status:
            print(response.headers)
        else:
            print('不是200')
