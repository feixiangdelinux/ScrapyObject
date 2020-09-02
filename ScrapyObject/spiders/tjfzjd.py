# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider tjfzjd www.tjfzjd.com
# 运行爬虫ok
# scrapy crawl tjfzjd -o tjfzjd.json
class TjfzjdSpider(scrapy.Spider):
    name = 'tjfzjd'
    website = 'tjfzjd'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.tjfzjd.com/']
    start_urls = ['http://www.tjfzjd.com/index.php/vod/type/id/7.html']

    # start_urls = ['http://www.tjfzjd.com/index.php/vod/play/id/133541/sid/1/nid/1.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?M3U8|http.*?MP4|http.*?WMV|http.*?MOV|http.*?AVI|http.*?MKV|http.*?FLV|http.*?RMVB|http.*?3GP',
            content, re.IGNORECASE)
        if len(video_url):
            if '\\' in video_url[0]:
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
        pUrl = response.xpath("//a[@class='cover']//img/@ src").extract()
        if len(pUrl):
            name = response.xpath("//a[@class='cover']//img/@ alt").extract()
            tags = response.xpath("//div[@class='title']//h1/text()").extract()
            url = response.xpath("//a[@class='cover']/@ href").extract()
            for k in pUrl:
                id_list = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[id_list]
                item['url'] = url[id_list]
                item['tags'] = tags[0]
                item['pUrl'] = split_joint('http://www.' + self.website + '.buzz/', k)
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
