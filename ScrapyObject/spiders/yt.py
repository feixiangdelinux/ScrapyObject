# -*- coding: utf-8 -*-
import urllib

from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# http://www.yt152.com/
# 创建爬虫
# scrapy genspider yt www.yt152.com
# 运行爬虫
# scrapy crawl yt -o yt.json
class YtSpider(scrapy.Spider):
    name = 'yt'
    website = 'yt152'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.yt152.com/']
    start_urls = ['http://www.yt152.com/vod-play-id-200411-src-1-num-1.html']

    # start_urls = ['http://www.yt152.com/vod-type-id-16-pg-6.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'http.*?\.M3U8', content, re.IGNORECASE)
        if len(video_url):
            if '\'' not in video_url[0] and video_url[0].startswith('http'):
                tag = response.xpath("//div[@style='margin-top:3px;']//a/text()").extract()
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['url'] = response.url
                item['tags'] = tag[1]
                item['vUrl'] = urllib.parse.unquote(video_url[0])
                item['name'] = ''
                item['pUrl'] = ''
                self.i = self.i + 1
                yield item
        url = response.xpath("//div[@class='col-xs-6 col-md-3 col-lg-3']//div//a/@ href").extract()
        name = response.xpath("//img[@style='max-height:126px;']/@ alt").extract()
        if len(url) and len(name):
            pUrl = response.xpath("//img[@style='max-height:126px;']/@ data-original").extract()
            for k in url:
                position = url.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['url'] = split_joint('http://www.' + self.website + '.com/', url[position])
                if '|' in name[position]:
                    item['name'] = name[position][:name[position].index("|")]
                else:
                    item['name'] = name[position]
                item['pUrl'] = pUrl[position]
                item['tags'] = ''
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
