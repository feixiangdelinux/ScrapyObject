# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.aea3b92f6415.com/index/home.html
# 创建爬虫
# scrapy genspider acb www.acb9276ce215.com
# 运行爬虫
# scrapy crawl acb -o acb.json
class AcbSpider(scrapy.Spider):
    name = 'acb'
    website = 'aea3b92f6415'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/index/home.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = response.xpath("//script/text()").extract()
        if len(video_url):
            if 'var video' in video_url[0]:
                pattern = re.compile("'(.*)'")
                str_re1 = pattern.findall(video_url[0])
                if str_re1[0].startswith('/'):
                    if 'https://' in str_re1[1]:
                        item = VideoBean()
                        item['id'] = self.i
                        item['e'] = ''
                        item['i'] = '0'
                        item['name'] = ''
                        item['url'] = response.url
                        item['tags'] = ''
                        item['pUrl'] = ''
                        item['vUrl'] = str_re1[1] + str_re1[0]
                        self.i = self.i + 1
                        yield item
                    if 'https://' in str_re1[2]:
                        item = VideoBean()
                        item['id'] = self.i
                        item['e'] = ''
                        item['i'] = '0'
                        item['name'] = ''
                        item['url'] = response.url
                        item['tags'] = ''
                        item['pUrl'] = ''
                        item['vUrl'] = str_re1[2] + str_re1[0]
                        self.i = self.i + 1
                        yield item
                    if 'https://' in str_re1[3]:
                        item = VideoBean()
                        item['id'] = self.i
                        item['e'] = ''
                        item['i'] = '0'
                        item['name'] = ''
                        item['url'] = response.url
                        item['tags'] = ''
                        item['pUrl'] = ''
                        item['vUrl'] = str_re1[3] + str_re1[0]
                        self.i = self.i + 1
                        yield item
        name = response.xpath("//li[@class='content-item']//a/@ title").extract()
        tag = response.xpath("//div[@class='box cat_pos clearfix']//span//a/text()").extract()
        if len(name) and len(tag):
            url = response.xpath("//li[@class='content-item']//a/@ href").extract()
            for k in name:
                position = name.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = k
                item['url'] = split_joint('https://www.' + self.website + '.com/', url[position])
                item['tags'] = tag[-1]
                item['pUrl'] = 'https://jsjs.qcyn72.com/10/assets/images/default/loading/235x140.jpg'
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('https://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)