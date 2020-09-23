# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *
# https://xf.002xf.com/
# 创建爬虫
# scrapy genspider xf xf.002xf.com
# 运行爬虫ok
# scrapy crawl xf -o xf.json
class XfSpider(scrapy.Spider):
    name = 'xf'
    allowed_domains = ['xf.002xf.com']
    # start_urls = ['http://xf.002xf.com/']
    start_urls = ['https://xf.002xf.com/play/20341/1/1.html']

    def parse(self, response):
        content = get_data(response)
        name = response.xpath("//script[@type='text/javascript']/text()").extract()
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            name[-1], re.IGNORECASE)
        print(video_url)
