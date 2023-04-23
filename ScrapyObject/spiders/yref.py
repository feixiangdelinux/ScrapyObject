# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

''''
已完成
scrapy crawl yref -o yref.json
http://iin.yref11.top/
'''


class YrefSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://iin.'
    # 中缀
    website = 'yref11'
    # 后缀
    suffix = '.top/'
    name = 'yref'
    allowed_domains = [website + '.top']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        else:
            name = response.xpath("//div[@class='item tyui']//div[@class='playlist collapse in']//div//div//img/@ alt").extract()
            p_url = response.xpath("//div[@class='item tyui']//div[@class='playlist collapse in']//div//div//img/@ src").extract()
            tag = response.xpath("//div[@class='item tyui']//p/text()").extract()
            url = response.xpath("//ul[@class='playlistlink-1 clearfix']//li//a/@ href").extract()
            if len(name) and len(p_url) and len(tag) and len(url):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tag[0][tag[0].index(':') + 1:].strip(), url=split_joint(self.prefix + self.website + self.suffix, url[0]), name=name[0], pUrl=p_url[0], vUrl='')
        url_list = get_url(content)
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
