# -*- coding: utf-8 -*-

from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl uu -o uu.json
https://992kp5.kkpp6zz.xyz/index.html
'''


class UuSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://992kp5.'
    # 中缀
    website = 'kkpp6zz'
    # 后缀
    suffix = '.xyz/'
    name = 'uu'
    allowed_domains = [website + '.xyz']
    start_urls = [prefix + website + suffix + 'index.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'\(.*?\.M3U8', content, re.IGNORECASE)
        pUrls = re.findall(r'get_img_url.*?"\),', content, re.IGNORECASE)
        names = response.xpath("//div[@class='ttss1 navv_obxobx']//a/text()").extract()
        if len(video_url) and len(pUrls) and len(names):
            video_url = video_url[0]
            if '"' in video_url:
                self.i = self.i + 1
                video_url = video_url[video_url.index('"') + 1:].strip()
                yield get_video_item(id=self.i, tags=names[-2], url='', name=names[-1], pUrl='https://992i2382.com' + pUrls[0][13:-3], vUrl='https://ch22dv78.com' + video_url)
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
