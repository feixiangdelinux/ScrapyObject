# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider zzhmtyn www.7mx2.com
# 运行爬虫
# scrapy crawl msp -o msp.json
# 不能用
class MspSpider(scrapy.Spider):
    website = '7mx3'
    name = 'msp'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.' + website + '.com/']
    # start_urls = ['http://www.7mx3.com/']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'[a-zA-z]+://[^\s]*(?i)AVI|[a-zA-z]+://[^\s]*(?i)MOV|[a-zA-z]+://[^\s]*(?i)WMV|[a-zA-z]+://[^\s]*('
            r'?i)3GP|[a-zA-z]+://[^\s]*(?i)MKV|[a-zA-z]+://[^\s]*(?i)FLV|[a-zA-z]+://[^\s]*(?i)RMVB|[a-zA-z]+://['
            r'^\s]*(?i)MP4|[a-zA-z]+://[^\s]*(?i)M3u8',
            content)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            title_prefix = response.xpath('/html/head/title/text()').extract()[0]
            item['name'] = title_prefix[:-21]
            item['url'] = response.xpath("//link[@rel='canonical']/@ href").extract()[0]
            tag = response.xpath("//meta[@property='video:tag']/@ content").extract()[0]
            if len(tag) == 0:
                item['tags'] = "综合"
            else:
                item['tags'] = tag
            item['pUrl'] = response.xpath("//video[@id='player']/@ poster").extract()[0]
            item['vUrl'] = video_url[0]
            self.i = self.i + 1
            yield item

        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css'):
                if url.startswith('/'):
                    full_url = split_joint('http://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
