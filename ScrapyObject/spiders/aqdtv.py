# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider aqdtv www.aqdtv131.com
# 运行爬虫
# scrapy crawl aqdtv -o aqdtv.json
# https://siyou.nos-eastchina1.126.net/21/roomlist.json
class AqdtvSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '35bc3'
    # 后缀
    suffix = '.com/'
    name = 'aqdtv'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix + 'index/home.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 整理视频数据
        video_suffix = re.findall(r'var video.*?;', content, re.IGNORECASE)
        url_list = response.xpath("//div[@id='tpl-img-content']//li//a[@target='_blank']/@ href").extract()
        if len(video_suffix):
            tag_list = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
            pattern = re.compile(r"\'(.*?)\'")
            video_url_suffix = pattern.findall(video_suffix[0])
            video_prefix = re.findall(r'm3u8_host.*?;', content, re.IGNORECASE)
            for url in video_prefix:
                pattern = re.compile(r"\'(.*?)\'")
                video_url_prefix = pattern.findall(url)
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tag_list[-2], url=response.url,
                                     vUrl=video_url_prefix[0] + video_url_suffix[0])
        elif len(url_list):
            name_list = response.xpath("//div[@id='tpl-img-content']//li//a[@target='_blank']/@ title").extract()
            pic_list = response.xpath(
                "//div[@id='tpl-img-content']//li//a[@target='_blank']// img[@class='lazy']/@ data-original").extract()
            if len(url_list) == len(pic_list) == len(pic_list):
                for index, value in enumerate(url_list):
                    self.i = self.i + 1
                    yield get_video_item(id=self.i, url=split_joint(self.prefix + self.website + self.suffix, value),
                                         name=name_list[index], pUrl=pic_list[index])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
