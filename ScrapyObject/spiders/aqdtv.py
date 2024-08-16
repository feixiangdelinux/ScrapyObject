# -*- coding: utf-8 -*-

from ScrapyObject.spiders.utils.url_utils import *

'''
网站似乎失效
scrapy crawl aqdtv -o aqdtv.json
https://www.jpds6.pics/cn/home/web/

https://ddi.avnyg4.makeup/cn/home/web/
https://lsu.avdz9.motorcycles/cn/home/web/
https://qxe.lkhsp9.hair/lkhsp/


https://bxp.avjingling3.yachts/cn/home/web/

'''
class AqdtvSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://ddi.'
    # 中缀
    website = 'avnyg4'
    # 后缀
    suffix = '.makeup/'
    name = 'aqdtv'
    allowed_domains = [website + '.makeup']
    start_urls = [prefix + website + suffix + '/cn/home/web/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        tag_list = response.xpath("//div[@class='inputA']//span/text()").extract()
        if len(video_url) and len(tag_list):
            self.i = self.i + 1
            mTag = tag_list[-1][tag_list[-1].index('标签：') + 3:-1].strip()
            if ',' in mTag:
                mTag = mTag[mTag.rfind(',') + 1:]
            yield get_video_item(id=self.i, tags=mTag, url=response.url, vUrl=video_url[-1])
        url_list = response.xpath("//div[@class='col-md-3 portfolio-item new-video']//a/@ href").extract()
        name_list = response.xpath("//div[@class='col-md-3 portfolio-item new-video']//a/@ title").extract()
        pUrl_list = response.xpath("//div[@class='col-md-3 portfolio-item new-video']//a//img/@ src").extract()
        if len(url_list) and len(name_list) and len(pUrl_list):
            if len(url_list) == len(name_list) and len(url_list) == len(pUrl_list) * 2:
                for index, value in enumerate(pUrl_list):
                    self.i = self.i + 1
                    yield get_video_item(id=self.i, url=split_joint(self.prefix + self.website + self.suffix, url_list[index * 2]), name=name_list[index * 2], pUrl=value)
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
