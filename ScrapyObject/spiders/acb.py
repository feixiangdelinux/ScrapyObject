# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

# 运行爬虫
# scrapy crawl acb -o acb.json
class AcbSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '3b5g8'
    # 后缀
    suffix = '.com/'
    name = 'acb'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.3b5g8.com/index/home.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        aa = re.findall(r'var m3u8_host.*?;', content, re.IGNORECASE)
        bb = re.findall(r'const dplayer_video_url.*?;', content, re.IGNORECASE)
        if len(aa) and len(bb):
            cc = re.findall(re.compile(r"'(.*?)'"), aa[0])[0] + re.findall(re.compile(r"'(.*?)'"), bb[0])[0]
            name = response.xpath("//div[@class='row title-row']//h3/text()").extract()
            tags = response.xpath("//span[@class='info-time']//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0], tags=tags[0], url="", pUrl="https://bkimg.cdn.bcebos.com/pic/3bf33a87e950352a87460b265043fbf2b2118bfc", vUrl=cc)
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
