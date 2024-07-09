# -*- coding: utf-8 -*-
import urllib.parse

from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
scrapy crawl ya -o ya.json
https://21maoaj.com/index.html
'''


class YaSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '21maoaj'
    # 后缀
    suffix = '.com/'
    name = 'ya'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix + 'index.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=urllib.parse.unquote(format_url_one(video_url[0])))
        url_list = response.xpath("//a[@class='video-pic loading']/@href").extract()
        name_list = response.xpath("//a[@class='video-pic loading']/@title").extract()
        pic_list = response.xpath("//a[@class='video-pic loading']//img/@data-original").extract()
        tag_list = response.xpath("//div[@class='box cat_pos clearfix']//span//a/text()").extract()
        if len(name_list) and len(pic_list) and len(tag_list) and len(url_list) and len(tag_list) == 2:
            for index, value in enumerate(pic_list):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tag_list[-1], url=split_joint(self.prefix + self.website + self.suffix, url_list[index]), name=name_list[index], pUrl=pic_list[index], vUrl='')
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
