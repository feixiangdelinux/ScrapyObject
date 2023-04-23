# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
修改settings.py里# DOWNLOAD_DELAY = 3
改成1,意思是一秒访问一次
DOWNLOAD_DELAY = 1

scrapy crawl hsex -o hsex.json
https://hsex.icu/
'''


class HsexSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'hsex'
    # 后缀
    suffix = '.icu/'
    name = "hsex"
    allowed_domains = [website + '.icu']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        name = response.xpath("//h3[@class='panel-title']/text()").extract()
        p_url = response.xpath("//video[@id='video-play']/@ poster").extract()
        v_url = response.xpath("//source[@type='application/x-mpegURL']/@ src").extract()
        if len(p_url) and len(v_url) and len(name):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='综合', url=response.url, name=name[0], pUrl=p_url[0], vUrl=v_url[0][:v_url[0].index('?')])
        url_list = get_url(content)
        for url in url_list:
            if url.endswith('.htm'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
