# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider oumeidy oumeidy1.com
# 运行爬虫
# scrapy crawl zzhmtyn -o zzhmtyn.json
class ZzhmtynSpider(scrapy.Spider):
    name = 'zzhmtyn'
    website = 'zzhmtyn188'
    allowed_domains = [website + '.com']
    start_urls = ['http://www.' + website + '.com/']

    # start_urls = ['http://zzhmtyn188.com/video/14891.html?14891-0-0']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = response.xpath("//div[@id='content_jr']//script[@type='text/javascript']/@ src").extract()
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            title_prefix = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
            item['name'] = title_prefix[-1]
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = split_joint('http://' + self.website + '.com/', video_url[0])
            self.i = self.i + 1
            yield item
        else:
            url = response.xpath("//a[@title='在线播放']/@ href").extract()
            if len(url):
                title_prefix = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
                pUrl = response.xpath("//dt//img/@ src").extract()
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = title_prefix[-1]
                item['url'] = split_joint('http://' + self.website + '.com/', url[0])
                item['tags'] = title_prefix[-2]
                item['pUrl'] = pUrl[0]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
