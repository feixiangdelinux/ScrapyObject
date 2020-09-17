# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider ub www.ub81.me
# 运行爬虫ok
# scrapy crawl ub -o ub.json
# https://ub22.me/
class UbSpider(scrapy.Spider):
    name = 'ub'
    website = 'ub22'
    allowed_domains = [website + '.me']
    start_urls = ['https://' + website + '.me']

    # start_urls = ['https://ub22.me/vodplayhtml/11941/index_1_1.html']
    # start_urls = ['https://ub22.me/vodtypehtml/12/']
    # start_urls = ['https://ub22.me/template/9999ak/helpme/android.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        if len(video_url):
            tag = response.xpath("//div[@class='title']//a/text()").extract()
            name = response.xpath("//div[@id='hellobox']//div[@class='title']//h1/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = video_url[0]
            for k in name:
                if '正在播放：' in k:
                    item['name'] = k[5:]
            item['tags'] = tag[1]
            item['pUrl'] = ''
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//div[@class='vodpic lazyload']/@ data-original").extract()
        name = response.xpath("//div[@class='vodname']/text()").extract()
        if len(pUrl) and len(name):
            for k in pUrl:
                position = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[position]
                item['url'] = ''
                if pUrl[position].startswith('//'):
                    item['pUrl'] = 'https:' + pUrl[position]
                else:
                    item['pUrl'] = pUrl[position]
                item['vUrl'] = ''
                item['tags'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and url != '/' and '"' not in url and '\'' not in url and 'javascript' not in url and '#' not in url:
                if url.startswith('/'):
                    full_url = split_joint('https://' + self.website + '.me/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
