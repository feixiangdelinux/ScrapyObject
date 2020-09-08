# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider fqypzxxx www.fqypzxxx.com
# 运行爬虫ok
# scrapy crawl fqypzxxx -o fqypzxxx.json
# ok
class FqypzxxxSpider(scrapy.Spider):
    name = 'fqypzxxx'
    website = 'fqypzxxx'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.fqypzxxx.com/']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//div[@class='film_info clearfix']//img/@ src").extract()
        if len(pUrl):
            tag = response.xpath("//div[@class='box cat_pos clearfix']//a/text()").extract()
            url = response.xpath("//div[@class='film_bar clearfix']//a/@ href").extract()
            name = response.xpath("//dd[@class='film_title']/text()").extract()
            for k in url:
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[0]
                item['url'] = split_joint('http://www.' + self.website + '.com/', k)
                item['tags'] = tag[-1]
                item['pUrl'] = pUrl[0]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        video_url = re.findall(
            r'https.*?\.M3U8|https.*?\.MP4|https.*?\.WMV|https.*?\.MOV|https.*?\.AVI|https.*?\.MKV|https.*?\.FLV|https.*?\.RMVB|https.*?\.3GP',
            content, re.IGNORECASE)
        if len(video_url) and '"' not in video_url[0]:
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = video_url[0].replace("\\/", "/")
            item['name'] = ''
            item['tags'] = ''
            item['pUrl'] = ''
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and 'www.' not in url and 'javascript' not in url:
                if url.startswith('/'):
                    full_url = split_joint('http://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
