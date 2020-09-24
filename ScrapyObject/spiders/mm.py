# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# http://www.840mm.com
# 创建爬虫
# scrapy genspider mm www.840mm.com
# 运行爬虫
# scrapy crawl mm -o mm.json
class MmSpider(scrapy.Spider):
    name = 'mm'
    website = '840mm'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.840mm.com/']
    # start_urls = ['http://www.840mm.com/play/index148687-0-0.html']
    # start_urls = ['http://www.840mm.com/view/index111192.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[0]
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//div[@class='col-md-9']//img/@ src").extract()
        name = response.xpath("//div[@class='col-md-9']//img/@ title").extract()
        url = response.xpath("//a[@target='_self']/@ href").extract()
        tags = response.xpath("//div[@class='info']//p//a/text()").extract()
        if len(pUrl):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0]
            item['url'] = split_joint('http://www.' + self.website + '.com/', url[0])
            item['tags'] = tags[0]
            item['pUrl'] = pUrl[0]
            item['vUrl'] = ''
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
