# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *

# 创建爬虫
# scrapy genspider dm www.dm528.com
# 运行爬虫ok
# scrapy crawl dm -o dm.json
class DmSpider(scrapy.Spider):
    name = 'dm'
    website = 'dm528'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.dm528.com/']
    # start_urls = ['http://www.dm528.com/?m=vod-play-id-13600-src-1-num-1.html']
    start_urls = ['http://www.dm528.com/?m=vod-type-id-5.html']
    def __init__(self):
        global website
        self.i = 1
    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content,
            re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[0].replace("\\/", "/")
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//div[@class='thumbnail']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//div[@class='thumbnail']//a/@ href").extract()
            # tags = response.xpath("//div[@class='media']//dt/text()").extract()[-2][4:]
            name = pUrl = response.xpath("//div[@class='thumbnail']//img/text()").extract()
            print(name)
