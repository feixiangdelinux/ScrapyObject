# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# https://www.jkwhu8.de/play.x?stype=mlmoviehd&movieid=2686
# 创建爬虫
# scrapy genspider jkwhu www.jkwhu8.de
# 运行爬虫
# scrapy crawl jkwhu -o jkwhu.json
class JkwhuSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'qkzy5g'
    # 后缀
    suffix = '.de/'
    name = 'jkwhu'
    allowed_domains = ['www.' + website + '.de']
    start_urls = [prefix + website + suffix+'home.htm']
    # start_urls = ['https://www.qkzy5g.de/home.htm']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        # 从网页中提取url链接
        url_list = get_url(content)
        # 整理视频数据
        video_url_one = response.xpath("//span[@class='hiddenBox']/text()").extract()
        if len(video_url_one):
            video_url = re.findall(r'"(.*)"', response.xpath("//script/text()").extract()[0], re.IGNORECASE)
            if len(video_url):
                final_video_url = list(set(video_url))
                for k in final_video_url:
                    if 'http' in k and '","' in k:
                        aa = k.split('","')
                        for b in aa:
                            self.i = self.i + 1
                            yield get_video_item(id=self.i, url=response.url, vurl=split_joint(b, video_url_one[0]))
        # 整理图片数据
        pic_url = response.xpath("//li[@class='col-md-3 col-sm-6 col-xs-12']//a/@ data-original").extract()
        name = response.xpath(
            "//li[@class='col-md-3 col-sm-6 col-xs-12']//a[@class='video-pic loading']/@ title").extract()
        tags = response.xpath("//h3[@class='m-0']/text()").extract()
        url = response.xpath(
            "//li[@class='col-md-3 col-sm-6 col-xs-12']//a[@class='video-pic loading']/@ href").extract()
        if len(pic_url) and len(tags):
            for k in pic_url:
                position = pic_url.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[position],
                                     url=split_joint(self.prefix + self.website + self.suffix, url[position]),
                                     tags=tags[0], purl=k)
        # 提取url
        for url in url_list:
            if not url.endswith(
                    '.css') and url != '/' and '"' not in url and '\'' not in url and 'javascript' not in url and '#' not in url:
                if url.startswith('/'):
                    yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)