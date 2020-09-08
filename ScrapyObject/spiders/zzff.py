# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *

# 创建爬虫
# scrapy genspider zzff www.zzff6.com
# 运行爬虫ok
# scrapy crawl zzff -o zzff.json
class ZzffSpider(scrapy.Spider):
    name = 'zzff'
    website = 'zzff9'
    allowed_domains = [website + '.com']
    start_urls = ['https://zzff9.com/']
    # start_urls = ['https://zzff9.com/video/show/id/37519']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        name = response.xpath("//div[@class='gc_vidoe_nav']//a/text()").extract()
        if len(video_url) and len(name):
            pUrl = re.findall(
                r'picurl .*?;',
                content, re.IGNORECASE)
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = video_url[0]
            item['name'] = name[-1]
            item['tags'] = name[-2][:-3]
            item['pUrl'] = pUrl[0][10:-2]
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.ico') and not url.endswith(
                    '.css') and url != '/' and '"' not in url and 'javascript' not in url and '#' not in url:
                if url.startswith('/'):
                    full_url = split_joint('https://' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
