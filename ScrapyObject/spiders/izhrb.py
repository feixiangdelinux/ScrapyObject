# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider izhrb www.iz2hrb.top
# 运行爬虫ok
# scrapy crawl izhrb -o izhrb.json
class IzhrbSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = 'tq8164'
    # 后缀
    suffix = '.top/'
    name = 'izhrb'
    allowed_domains = ['www.' + website + '.top']
    start_urls = [prefix + website + suffix]

    # start_urls = ['https://www.tq8164.top/home.htm']

    def start_requests(self):
        for num in range(0, 21):
            yield scrapy.Request(self.prefix + self.website + self.suffix + "mlvideolist.x?tagid=%d" % num,
                                 callback=self.parse)
            yield scrapy.Request(self.prefix + self.website + self.suffix + "mlmovielisthd.x?classid=%d" % num,
                                 callback=self.parse)
            yield scrapy.Request(self.prefix + self.website + self.suffix + "mlmovielist.x?tagid=%d" % num,
                                 callback=self.parse)
        yield scrapy.Request(self.prefix + self.website + self.suffix + "zpmp4list.x?tagid=", callback=self.parse)

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        pic_url = response.xpath("//a[@class='video-pic loading']/@ data-original").extract()
        if len(pic_url):
            url = response.xpath("//a[@class='video-pic loading']/@ href").extract()
            name = response.xpath("//a[@class='video-pic loading']/@ title").extract()
            for k in pic_url:
                id_list = pic_url.index(k)
                self.i = self.i + 1
                yield get_video_item(id=self.i, name=name[id_list],
                                     url=split_joint(self.prefix + self.website + self.suffix, url[id_list]), purl=k)
        video_url = response.xpath("//span[@id='vpath']/text()").extract()
        if len(video_url):
            video_prefix = re.findall(r'm3u8path=.*?;', content, re.IGNORECASE)
            tag = response.xpath("//div[@class='player_title']//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, tags=tag[-1],
                                 vurl=split_joint(video_prefix[-1].replace('m3u8path="', '').replace('";', ''),
                                                  video_url[0]))
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and 'javascript' not in url and url != '/' and url != '#':
                if url.startswith('/'):
                    yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url),
                                         callback=self.parse)
                elif url.startswith('?'):
                    yield scrapy.Request(split_joint(response.url[:response.url.index('?')], url), callback=self.parse)
                elif url.startswith('http') or url.startswith('www'):
                    yield scrapy.Request(url, callback=self.parse)
