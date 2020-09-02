# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider wujing www.wujing365.com
# 运行爬虫ok
# scrapy crawl wujing -o wujing.json
class WujingSpider(scrapy.Spider):
    name = 'wujing'
    website = 'wujing365'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.' + website + '.com']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//div[@class='media']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//dt[@class='playurl2']//a/@ href").extract()
            tags = response.xpath("//div[@class='media']//dt/text()").extract()[-2][4:]
            name = response.xpath("//div[@class='media']//dt/text()").extract()[2][3:]
            for k in urls:
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name
                item['url'] = split_joint('http://www.' + self.website + '.com/', k)
                if len(tags):
                    item['tags'] = tags
                else:
                    item['tags'] = '综合'
                item['pUrl'] = split_joint('http://www.' + self.website + '.com/', pUrl[0])
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        video_url = re.findall(
            r'http.*?M3U8|http.*MP4|http.*WMV|http.*MOV|http.*AVI|http.*MKV|http.*FLV|http.*RMVB|http.*3GP', content,
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
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and not url.endswith(
                    '.ico') and url != '/' and 'javascript' not in url and '<a' not in url:
                full_url = split_joint('http://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
