# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
scrapy crawl se -o se.json
https://94se.net
'''


class SeSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '94se'
    # 后缀
    suffix = '.net/'
    name = 'se'
    allowed_domains = [website + '.net']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        v_url_list = response.xpath("//video[@id='video']//source/@ src").extract()
        if len(v_url_list):
            self.i = self.i + 1
            name = ''
            p_url = response.xpath("//meta[@property='og:image']/@ content").extract()
            name_list = response.xpath('/html/head/title/text()').extract()
            tag_list = response.xpath("//div[@class='videos']//h4//a/text()").extract()
            if len(name_list):
                if name_list[0].find('- 94色') != -1:
                    name = name_list[0][0:name_list[0].index('- 94色')]
                else:
                    name = name_list[0].strip()
            yield get_video_item(id=self.i, tags=tag_list[0].strip(), url=response.url, name=name, pUrl=p_url[0], vUrl=v_url_list[0])
        is_empty = response.xpath("//ul//li").extract()
        # 页面是否是空页面
        if len(is_empty):
            # 从网页中提取url链接
            url_list = get_url(content)
            # 提取url
            for url in url_list:
                if url.endswith('.html') and url.startswith('/'):
                    yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
