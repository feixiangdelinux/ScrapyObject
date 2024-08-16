# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
网站需要翻墙
scrapy crawl hbsy -o hbsy.json
https://www.dym03.cc:2008/
'''


class HbsySpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'dym03'
    # 后缀
    suffix = '.cc:2008/'
    name = 'hbsy'
    allowed_domains = [website + '.cc']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        v_url_list = re.findall(r'=http.*?\.m3u8', content, re.IGNORECASE)
        if len(v_url_list):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=v_url_list[0][1:])
        pUrls = response.xpath("//div[@class='col-md-9']//img/@ src").extract()
        names = response.xpath("//div[@class='col-md-9']//img/@ title").extract()
        tags = response.xpath("//div[@class='info']//p//a/text()").extract()
        urls = response.xpath("//a[@title='在线播放']/@ href").extract()
        if len(pUrls) and len(names) and len(tags) and len(urls):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[0], url=split_joint(self.prefix + self.website + self.suffix, urls[0]), name=names[0], pUrl=pUrls[0], vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
