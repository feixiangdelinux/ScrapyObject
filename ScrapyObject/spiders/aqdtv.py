# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# https://www.aqdtv131.com/
# 创建爬虫
# scrapy genspider aqdtv www.aqdtv131.com
# 运行爬虫
# scrapy crawl aqdtv -o aqdtv.json
class AqdtvSpider(scrapy.Spider):
    name = 'aqdtv'
    website = 'aqdtv131'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.aqdtv131.com/']
    # start_urls = ['https://www.aqdtv131.com/videos/play/9407']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        pUrl = re.findall(r'pic : \'.*?\'', content, re.IGNORECASE)
        if len(video_url) and len(pUrl):
            name = response.xpath("//ol[@class='breadcrumb']//li/text()").extract()
            tags = response.xpath("//ol[@class='breadcrumb']//li//a/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0]
            item['url'] = response.url
            item['tags'] = tags[-1]
            item['pUrl'] = pUrl[0][7:-1]
            item['vUrl'] = video_url[0]
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and 'www.' not in url and 'javascript' not in url:
                if url.startswith('/'):
                    full_url = split_joint('https://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)
