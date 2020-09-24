# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# http://ddxx88.com/htm/mv9/73589.htm
# 创建爬虫
# scrapy genspider ddxx ddxx88.com
# 运行爬虫
# scrapy crawl ddxx -o ddxx.json
class DdxxSpider(scrapy.Spider):
    name = 'ddxx'
    website = 'ddxx88'
    allowed_domains = [website + '.com']
    start_urls = ['http://ddxx88.com/']

    # start_urls = ['http://xf.ddxx88.com/htm/mvplay9/73589.htm']
    # start_urls = ['http://ddxx88.com/htm/mv9/73589.htm']
    # start_urls = ['http://ddxx88.com/htm/Movie9/']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url_one = response.xpath(
            "//div[@class='col-md-9 col-sm-12 col-xs-12 player_left max']//script//text()").extract()
        if len(video_url_one) and 'var src =' in video_url_one[0]:
            video_url = re.findall(
                r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
                video_url_one[-1], re.IGNORECASE)
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[0].replace("\\/", "/")
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//div[@class='col-md-9']//img/@ src").extract()
        if len(pUrl):
            url = response.xpath("//div[@class='play-list']//a/@ href").extract()
            name = response.xpath("//div[@class='player_title']//h1/text()").extract()
            tag = response.xpath("//div[@class='player_title']//div//a/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0]
            item['url'] = split_joint('http://' + self.website + '.com/', url[0])
            item['tags'] = tag[-1]
            item['pUrl'] = split_joint('http://' + self.website + '.com/', pUrl[0])
            item['vUrl'] = ''
            self.i = self.i + 1
            yield item
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.htm') and url.startswith('/'):
                full_url = split_joint('http://' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
