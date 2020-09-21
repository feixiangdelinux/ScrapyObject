# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider sundki www.sundki.com
# 运行爬虫ok
# scrapy crawl sundki -o sundki.json
# ok
class SundkiSpider(scrapy.Spider):
    name = 'sundki'
    website = 'sundki'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.sundki.com/']

    # start_urls = ['http://www.sundki.com/index.php/vod/type/id/35.html']
    # start_urls = ['http://www.sundki.com/index.php/vod/play/id/443712/sid/2/nid/1.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'[a-zA-z]+://[^\s]*?\.AVI|[a-zA-z]+://[^\s]*?\.MOV|[a-zA-z]+://[^\s]*?\.WMV|[a-zA-z]+://[^\s]*?\.3GP|[a-zA-z]+://[^\s]*?\.MKV|[a-zA-z]+://[^\s]*?\.FLV|[a-zA-z]+://[^\s]*?\.RMVB|[a-zA-z]+://[^\s]*?\.MP4|[a-zA-z]+://[^\s]*?\.M3U8',
            content, re.IGNORECASE)
        if len(video_url):
            name = response.xpath("//div[@class='head']//h3//a/text()").extract()
            tags = response.xpath("//li[@class='col-md-6 col-sm-6 hidden-xs padding-0']//a/text()").extract()
            pUrl = response.xpath("//meta[@itemprop='image']/@ content").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0]
            item['url'] = ''
            item['tags'] = tags[0]
            item['pUrl'] = pUrl[0]
            item['vUrl'] = video_url[0]
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
