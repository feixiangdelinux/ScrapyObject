# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider wujing www.wujing365.com
# 运行爬虫
# scrapy crawl wujing -o wujing.json
class WujingSpider(scrapy.Spider):
    name = 'wujing'
    website = 'wujing365'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.' + website + '.com']
    # start_urls = ['http://www.wujing365.com/?m=vod-type-id-1-pg-5.html']
    # start_urls = ['http://www.wujing365.com/?m=vod-detail-id-2470.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//dt//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//div[@class='playBar']//ul//li//a/@ href").extract()
            tags = response.xpath("//div[@class='position']//a/text()").extract()
            name = response.xpath("//dt//img/@ alt").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0]
            item['url'] = split_joint('http://www.' + self.website + '.com/', urls[0])
            item['tags'] = tags[-2]
            item['pUrl'] = pUrl[0]
            item['vUrl'] = ''
            self.i = self.i + 1
            yield item
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content,
            re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = format_url_one(video_url[0])
            item['name'] = ''
            item['tags'] = ''
            item['pUrl'] = ''
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
