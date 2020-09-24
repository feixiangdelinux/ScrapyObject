# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider dm www.dm528.com
# 运行爬虫
# scrapy crawl dm -o dm.json
# ok
class DmSpider(scrapy.Spider):
    name = 'dm'
    website = 'dm528'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.dm528.com/']
    # start_urls = ['http://www.dm528.com/?m=vod-play-id-13600-src-1-num-1.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content,
            re.IGNORECASE)
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
        pUrl = response.xpath("//div[@class='thumbnail']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//div[@class='thumbnail']//a/@ href").extract()
            tags = response.xpath("//div[@class='latest_title']/text()").extract()
            name = response.xpath("//div[@class='thumbnail']//img/@ title").extract()
            for k in pUrl:
                position = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[position]
                item['url'] = split_joint('http://www.' + self.website + '.com/', urls[position])
                item['tags'] = tags[0][2:]
                item['pUrl'] = pUrl[position]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html'):
                if url.startswith('/'):
                    full_url = split_joint('http://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
