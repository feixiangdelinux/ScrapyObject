# -*- coding: utf-8 -*-
from urllib import parse

from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider sisters http://23.244.60.225:1979/vod-play-id-37034-src-1-num-1.html
# 运行爬虫ok
# scrapy crawl sisters -o sisters.json
class SistersSpider(scrapy.Spider):
    name = 'sisters'
    website = '23.244.60.225:1979'
    allowed_domains = ['23.244.60.225']
    start_urls = ['http://' + website]

    # start_urls = ['http://23.244.60.225:1979/vod-play-id-37034-src-1-num-1.html/']
    # start_urls = ['http://23.244.60.225:1979/vod-detail-id-37034.html']
    # start_urls = ['http://23.244.60.225:1979/vod-type-id-1-pg-1.html']
    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http[^http]*?M3U8|http[^http]*?MP4|http[^http]*?WMV|http[^http]*?MOV|http[^http]*?AVI|http[^http]*?MKV|http[^http]*?FLV|http[^http]*?RMVB|http[^http]*?3GP',
            content, re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            title_prefix = response.xpath('/html/head/title/text()').extract()[0]
            item['name'] = title_prefix[5:-5]
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = parse.unquote(video_url[0])
            self.i = self.i + 1
            yield item
        else:
            pUrl = response.xpath("//div[@class='film_info clearfix']//img/@ src").extract()
            if len(pUrl):
                info = response.xpath("//div[@class='box cat_pos clearfix']//a/text()").extract()
                url = response.xpath("//a[@target='_blank' and @title='在线播放']/@ href").extract()
                for k in url:
                    item = VideoBean()
                    item['id'] = self.i
                    item['e'] = ''
                    item['i'] = '0'
                    item['name'] = info[-1]
                    item['url'] = split_joint('http://' + self.website + '/', k)
                    item['tags'] = info[0]
                    item['pUrl'] = pUrl[0]
                    item['vUrl'] = ''
                    self.i = self.i + 1
                    yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://' + self.website + '/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
