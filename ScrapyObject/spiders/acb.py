# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.aea3b92f6415.com/shipin/play-109933.html
# 创建爬虫
# scrapy genspider acb www.acb9276ce215.com
# 运行爬虫
# scrapy crawl acb -o acb.json
class AcbSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'aea3b92f6415'
    # 后缀
    suffix = '.com/'
    name = 'acb'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/index/home.html']
    # start_urls = ['https://www.aea3b92f6415.com/shipin/play-113142.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        video_url = response.xpath("//script/text()").extract()
        name = response.xpath("//meta[@name='keywords']/@ content").extract()
        tags = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
        # 整理视频数据
        video_url_one = get_video_url_one(content)
        if len(video_url_one) and len(name) and len(tags):
            l2 = list(set(video_url_one))
            self.i = self.i + 1
            for k in l2:
                yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1],
                                     purl='https://jsjs.qcyn72.com/10/assets/images/default/loading/235x140.jpg',
                                     vurl=k)
        if len(video_url):
            if 'var video' in video_url[0]:
                pattern = re.compile("'(.*)'")
                str_re1 = pattern.findall(video_url[0])
                if str_re1[0].startswith('/'):
                    if 'https://' in str_re1[1]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1],
                                             purl='https://jsjs.qcyn72.com/10/assets/images/default/loading/235x140.jpg',
                                             vurl=str_re1[1] + str_re1[0])
                    if 'https://' in str_re1[2]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1],
                                             purl='https://jsjs.qcyn72.com/10/assets/images/default/loading/235x140.jpg',
                                             vurl=str_re1[2] + str_re1[0])
                    if 'https://' in str_re1[3]:
                        self.i = self.i + 1
                        yield get_video_item(id=self.i, name=name[0], url=response.url, tags=tags[-1],
                                             purl='https://jsjs.qcyn72.com/10/assets/images/default/loading/235x140.jpg',
                                             vurl=str_re1[3] + str_re1[0])
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
