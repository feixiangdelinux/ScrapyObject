# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider sisters http://23.244.60.225:1979/vod-play-id-37034-src-1-num-1.html
# 运行爬虫ok
# scrapy crawl oumeid -o oumeid.json
# OumeidTextSpider
class OumeidSpider(scrapy.Spider):
    name = 'oumeid'
    website = 'oumeidy2'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.' + website + '.com/']
    start_urls = ['http://www.oumeidy1.com/vod-13608.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*M3U8|http.*MP4|http.*WMV|http.*MOV|http.*AVI|http.*MKV|http.*FLV|http.*RMVB|http.*3GP',
            content, re.IGNORECASE)
        if len(video_url):
            tags = response.xpath("//li[@class='active']//a/text()").extract()[0]
            pic = response.xpath("//video[@id='video']/@ poster").extract()[0]
            title_prefix = response.xpath('/html/head/title/text()').extract()[0]
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            if "-" in title_prefix:
                item['name'] = title_prefix[title_prefix.rindex("-") + 1:-1]
            else:
                item['name'] = title_prefix
            item['url'] = response.url
            item['tags'] = tags
            item['pUrl'] = pic
            item['vUrl'] = video_url[0].replace("\\/", "/")
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and '#' not in url and not url.endswith('.'):
                full_url = split_joint('http://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
