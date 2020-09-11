# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider leguatv www.leguatv.com
# 运行爬虫ok
# scrapy crawl leguatv -o leguatv.json

class LeguatvSpider(scrapy.Spider):
    name = 'leguatv'
    website = 'leguatv'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.leguatv.com/']
    # start_urls = ['https://www.leguatv.com/d/158562.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'[a-zA-z]+:[^\s]*\.AVI|[a-zA-z]+:[^\s]*\.MOV|[a-zA-z]+:[^\s]*\.WMV|[a-zA-z]+:[^\s]*\.3GP|[a-zA-z]+:[^\s]*\.MKV|[a-zA-z]+:[^\s]*\.FLV|[a-zA-z]+:[^\s]*\.RMVB|[a-zA-z]+:[^\s]*\.MP4|[a-zA-z]+:[^\s]*\.M3U8',
            content, re.IGNORECASE)
        url = response.xpath("//ul[@class='content_playlist list_scroll clearfix']//li//a/@ href").extract()
        neme_two = response.xpath("//ul[@class='content_playlist list_scroll clearfix']//li//a/text()").extract()
        if len(url):
            name = response.xpath("//a[@class='vodlist_thumb lazyload']/@ title").extract()
            pUrl = response.xpath("//a[@class='vodlist_thumb lazyload']/@ data-original").extract()
            for k in url:
                position = url.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[0] + neme_two[position]
                item['url'] = split_joint('https://www.' + self.website + '.com/', k)
                item['tags'] = ''
                item['pUrl'] = pUrl[0]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        if len(video_url):
            print(video_url)
            tag = response.xpath("//div[@class='play_text']//p//a/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = tag[-1]
            item['pUrl'] = ''
            item['vUrl'] = video_url[0].replace("\\/", "/")
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html'):
                if url.startswith('/'):
                    full_url = split_joint('https://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
