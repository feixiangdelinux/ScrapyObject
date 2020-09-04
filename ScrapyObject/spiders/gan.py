# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫gan
# scrapy genspider GanText www.734gan.com
# 运行爬虫ok
# scrapy crawl gan -o gan.json
# 网站关闭
class GanSpider(scrapy.Spider):
    name = 'gan'
    website = '849gan'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/']
    # start_urls = ['https://www.849gan.com/video/2020-6/51702.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'[a-zA-z]+://[^\s]*AVI|[a-zA-z]+://[^\s]*MOV|[a-zA-z]+://[^\s]*WMV|[a-zA-z]+://[^\s]*3GP|[a-zA-z]+://[^\s]*MKV|[a-zA-z]+://[^\s]*FLV|[a-zA-z]+://[^\s]*RMVB|[a-zA-z]+://[^\s]*MP4|[a-zA-z]+://[^\s]*M3U8',
            content, re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            title_prefix = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
            name = response.xpath("//span[@class='cat_pos_l']//font/text()").extract()
            item['name'] = name[-1]
            item['url'] = response.url
            item['tags'] = title_prefix[-1]
            item['pUrl'] = ''
            item['vUrl'] = video_url[-1]
            self.i = self.i + 1
            yield item
        else:
            pUrl = response.xpath("//a[@target='_blank']//img/@ src").extract()
            name = response.xpath("//a[@target='_blank']//img/@ title").extract()
            url = response.xpath("//a[@target='_blank']/@ href").extract()
            if len(pUrl):
                for k in pUrl:
                    id_list = pUrl.index(k)
                    item = VideoBean()
                    item['id'] = self.i
                    item['e'] = ''
                    item['i'] = '0'
                    item['name'] = name[id_list]
                    item['url'] = split_joint('https://www.' + self.website + '.com/', url[id_list])
                    item['tags'] = ''
                    item['pUrl'] = pUrl[id_list]
                    item['vUrl'] = ''
                    self.i = self.i + 1
                    yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and 'javascript' not in url:
                if url.startswith('/'):
                    full_url = split_joint('https://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
