# -*- coding: utf-8 -*-
from collections import OrderedDict

from ScrapyObject.spiders.utils.url_utils import *

'''
进行中
scrapy crawl xsmdl -o xsmdl.json
https://javmenu.one/zh


scrapy genspider lnalbumqqo https://lnalbumqqo.xyz

https://lnalbumqqo.xyz:16888/index.html


https://992i2382.com/20221202/89/891/891.mp4.m3u8
https://d.220zx.com/20221202/89/891/891.mp4.m3u8
https://d.220zx.com/20221202/89/891/891.mp4
https://992i2382.com/Uploads/vod/2022-12-02/891.mp4.gif
https://ch22dv78.com/20221202/89/891/891.mp4
https://ch22dv78.com/20221202/89/891/891.mp4.m3u8
https://ncdncd-sslmi.com/20240301/111/1111/1111.mp4
https://d.9xxav.com/20240301/111/1111/1111.mp4
'''


class XsmdlSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'javmenu'
    # 后缀
    suffix = '.one/'
    name = 'xsmdl'
    allowed_domains = [website + '.one']
    start_urls = [prefix + website + suffix + 'zh']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        tags = response.xpath("//span[@class='color-light-yellow']/text()").extract()
        urls = response.xpath("//div[@class='card-body p-2 p-md-3']//a/@href").extract()
        p_urls = response.xpath("//img[@class='card-img-top embed-responsive-item lazyload']/@data-src").extract()
        names = response.xpath("//p[@class='card-text text-primary']/@title").extract()
        if len(tags) and len(urls) and len(p_urls) and len(names):
            for index in range(len(p_urls)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0], url=urls[index + 1], name=names[index + 1], pUrl=p_urls[index], vUrl='')
        v_url_list = re.findall(r'http.*?\.M3U8', content, re.IGNORECASE)
        if len(v_url_list):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url='', name='', pUrl='', vUrl=v_url_list[0])
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('https'):
                yield scrapy.Request(url, callback=self.parse)
