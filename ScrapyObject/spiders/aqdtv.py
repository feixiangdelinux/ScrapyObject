# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.aqdtv131.com/
# 创建爬虫
# scrapy genspider aqdtv www.aqdtv131.com
# 运行爬虫
# scrapy crawl aqdtv -o aqdtv.json
class AqdtvSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'aqdtv131'
    # 后缀
    suffix = '.com/'
    name = 'aqdtv'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['https://www.aqdtv131.com/']
    # start_urls = ['https://www.aqdtv131.com/videos/play/9508']
    start_urls = ['https://www.aqdtv131.com/videos/play/1']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url = get_video_url_one(content)
        pic_url = re.findall(r'pic : \'.*?\'', content, re.IGNORECASE)
        if len(video_url) and len(pic_url):
            name = response.xpath("//ol[@class='breadcrumb']//li/text()").extract()
            tags = response.xpath("//ol[@class='breadcrumb']//li//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1], purl=pic_url[0][7:-1],
                                 vurl=video_url[0])
        # 提取url
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and 'www.' not in url and 'javascript' not in url:
                if url.startswith('/'):
                    full_url = split_joint(self.prefix + self.website + self.suffix, url)
                    yield scrapy.Request(full_url, callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)
