# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# http://www.uniwa.cc/
# 创建爬虫
# scrapy genspider uniwa www.uniwa.cc
# 运行爬虫ok
# scrapy crawl uniwa -o uniwa.json
class UniwaSpider(scrapy.Spider):
    name = 'uniwa'
    website = 'uniwa'
    allowed_domains = ['www.' + website + '.cc']
    start_urls = ['http://www.uniwa.cc/']
    # start_urls = ['http://www.uniwa.cc/video_conter-72475-14/index.html']
    # start_urls = ['http://www.uniwa.cc/video_detail-72475-14/index.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        name = response.xpath("//div[@class='video-title']//h2/text()").extract()
        if len(video_url) and len(name):
            print(video_url)
            tag = response.xpath("//p[@class='data ms-p margin-0']//a/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = video_url[0]
            item['name'] = name[0]
            item['tags'] = tag[0]
            item['pUrl'] = ''
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//img[@class='img-responsive']/@ src").extract()
        if len(pUrl):
            url = response.xpath("//a[@class='pic']/@ href").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = split_joint('http://www.' + self.website + '.cc/', url[0])
            item['pUrl'] = pUrl[0]
            item['vUrl'] = ''
            item['name'] = ''
            item['tags'] = ''
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://www.' + self.website + '.cc/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)