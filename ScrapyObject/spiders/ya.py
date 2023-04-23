# -*- coding: utf-8 -*-
import urllib.parse

from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
scrapy crawl ya -o ya.json
http://www.544ya.com/
'''


class YaSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '544ya'
    # 后缀
    suffix = '.com/'
    name = 'ya'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=urllib.parse.unquote(format_url_one(video_url[0])))
        else:
            name_list = response.xpath("//li[@class='col-md-2 col-sm-3 col-xs-4 ']//a[@class='video-pic loading']/@ title").extract()
            pic_list = response.xpath("//li[@class='col-md-2 col-sm-3 col-xs-4 ']//a[@class='video-pic loading']/@ style").extract()
            tag_list = response.xpath("//li[@class='col-md-2 col-sm-3 col-xs-4 ']//table//tr//td//div[@align='right']/text()").extract()
            url_list = response.xpath("//li[@class='col-md-2 col-sm-3 col-xs-4 ']//a[@class='video-pic loading']/@ href").extract()
            if len(name_list) and len(pic_list) and len(tag_list) and len(url_list):
                for index, value in enumerate(pic_list):
                    self.i = self.i + 1
                    yield get_video_item(id=self.i, tags=tag_list[index], url=split_joint(self.prefix + self.website + self.suffix, url_list[index]), name=name_list[index],
                                         pUrl=re.findall(r'http.*?\.jpg', pic_list[index], re.IGNORECASE)[0], vUrl='')
        url_list = get_url(content)
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
