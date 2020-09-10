# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider izhrb www.iz2hrb.top
# 运行爬虫ok
# scrapy crawl izhrb -o izhrb.json
# 可以

# IzhrbText
class IzhrbSpider(scrapy.Spider):
    name = 'izhrb'
    website = 'iz2hrb'
    allowed_domains = ['www.' + website + '.top']
    start_urls = ['http://www.iz2hrb.top/mlvideolist.x?tagid=3', 'http://www.iz2hrb.top/mlvideolist.x?tagid=7',
                  'http://www.iz2hrb.top/mlvideolist.x?tagid=2', 'http://www.iz2hrb.top/mlvideolist.x?tagid=1',
                  'http://www.iz2hrb.top/mlvideolist.x?tagid=5', 'http://www.iz2hrb.top/mlvideolist.x?tagid=6',
                  'http://www.iz2hrb.top/mlvideolist.x?tagid=8', 'http://www.iz2hrb.top/zpmp4list.x?tagid=',
                  'http://www.iz2hrb.top/mlmovielisthd.x?classid=4', 'http://www.iz2hrb.top/mlmovielisthd.x?classid=7',
                  'http://www.iz2hrb.top/mlmovielisthd.x?classid=5', 'http://www.iz2hrb.top/mlmovielisthd.x?classid=3',
                  'http://www.iz2hrb.top/mlmovielisthd.x?classid=6', 'http://www.iz2hrb.top/mlmovielisthd.x?classid=8',
                  'http://www.iz2hrb.top/mlmovielisthd.x?classid=2', 'http://www.iz2hrb.top/mlmovielisthd.x?classid=1',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=15', 'http://www.iz2hrb.top/mlvideolist.x?tagid=4',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=16', 'http://www.iz2hrb.top/mlmovielist.x?tagid=13',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=9', 'http://www.iz2hrb.top/mlmovielist.x?tagid=11',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=12', 'http://www.iz2hrb.top/mlmovielist.x?tagid=7',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=4', 'http://www.iz2hrb.top/mlmovielist.x?tagid=6',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=8', 'http://www.iz2hrb.top/mlmovielist.x?tagid=5',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=2', 'http://www.iz2hrb.top/mlmovielist.x?tagid=1',
                  'http://www.iz2hrb.top/mlmovielist.x?tagid=3']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//a[@class='video-pic loading']/@ data-original").extract()
        if len(pUrl):
            url = response.xpath("//a[@class='video-pic loading']/@ href").extract()
            name = response.xpath("//a[@class='video-pic loading']/@ title").extract()
            for k in pUrl:
                id_list = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['name'] = name[id_list]
                item['url'] = split_joint('http://www.' + self.website + '.top/', url[id_list])
                item['e'] = ""
                item['i'] = '0'
                item['pUrl'] = k
                item['tags'] = ""
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        video_url = response.xpath("//span[@id='vpath']/text()").extract()
        if len(video_url):
            video_prefix = re.findall(r'm3u8path=.*?;', content, re.IGNORECASE)
            tag = response.xpath("//div[@class='player_title']//a/text()").extract()
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['tags'] = tag[-1]
            item['vUrl'] = split_joint(video_prefix[-1].replace('m3u8path="', '').replace('";', ''), video_url[0])
            item['name'] = ''
            item['pUrl'] = ''
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and 'javascript' not in url and url != '/' and url != '#':
                if url.startswith('/'):
                    full_url = split_joint('http://www.' + self.website + '.top/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                elif url.startswith('?'):
                    full_url = split_joint(response.url[:response.url.index('?')], url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
