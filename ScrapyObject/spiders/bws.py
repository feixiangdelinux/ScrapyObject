# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# https://www.bws6.com/
# 创建爬虫
# scrapy genspider bws www.bws6.com
# 运行爬虫
# scrapy crawl bws -o bws.json
class BwsSpider(scrapy.Spider):
    name = 'bws'
    website = 'bws6'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.bws6.com/index/home.html']
    # start_urls = ['https://www.bws6.com/shipin/list-%E5%8A%A8%E6%BC%AB%E7%94%B5%E5%BD%B1-2.html']
    # start_urls = ['https://www.bws6.com/shipin/92059.html']
    # start_urls = ['https://www.bws6.com/shipin/play-92059.html?road=1']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',content, re.IGNORECASE)
        tags = response.xpath("//div[@class='pull-left text-left margin_left_10 pull-left-mobile2']//div//p/text()").extract()
        if len(video_url) and len(tags):
            name = response.xpath('/html/head/title/text()').extract()
            pUrl = response.xpath("//div[@class='pull-left pull-left-mobile1']//div//img/@ data-original").extract()
            for k in video_url:
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[0].strip()
                item['url'] = response.url
                item['tags'] = tags[0][3:]
                item['pUrl'] = pUrl[0]
                item['vUrl'] = k
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('https://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)

