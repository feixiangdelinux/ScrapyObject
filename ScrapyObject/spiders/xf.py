# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# https://xf.002xf.com/
# 创建爬虫
# scrapy genspider xf xf.002xf.com
# 运行爬虫
# scrapy crawl xf -o xf.json
class XfSpider(scrapy.Spider):
    name = 'xf'
    website = '002xf'
    allowed_domains = ['xf.' + website + '.com']
    start_urls = ['https://xf.002xf.com/']
    # start_urls = ['https://xf.002xf.com/play/9905/3/1.html']
    # start_urls = ['https://xf.002xf.com/YaZhoux/9905.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url_one = response.xpath("//script[@type='text/javascript']/text()").extract()
        if len(video_url_one) and 'var player_data=' in video_url_one[-1]:
            video_url = re.findall(
                r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
                video_url_one[-1], re.IGNORECASE)
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = format_url_one(video_url[0])
            self.i = self.i + 1
            yield item
        url = response.xpath("//p[@class='play-list']//a/@ href").extract()
        if len(url):
            name = response.xpath("//ul[@class='bread-crumbs']//li/text()").extract()
            tag = response.xpath("//ul[@class='bread-crumbs']//li//a/text()").extract()
            pUrl = response.xpath("//div[@class='detail-pic fn-left']//img/@ src").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[0][:-8]
            item['url'] = split_joint('http://xf.' + self.website + '.com/', url[0])
            item['tags'] = tag[-1]
            item['pUrl'] = split_joint('http://xf.' + self.website + '.com/', pUrl[0])
            item['vUrl'] = ''
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://xf.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
