# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider zzhmtyn www.7mx2.com
# 运行爬虫
# scrapy crawl msp -o msp.json
class MspSpider(scrapy.Spider):
    website = '7mx2'
    name = 'msp'
    allowed_domains = ['www.' + website + '.com']
    # start_urls = ['http://www.' + website + '.com/']

    start_urls = [
        'http://www.7mx2.com/8712/%E5%9B%BD%E5%86%85%E6%8D%A2%E5%A6%BB%E4%BF%B1%E4%B9%90%E9%83%A8%E6%B5%81%E5%87%BA%E8%A7%86%E9%A2%91-%E5%B7%A8%E4%B9%B3%E5%B0%91%E5%A6%87%E6%9C%8D%E4%BE%8D%E7%9C%9F%E5%85%A8%E9%9D%A2-%E6%B4%97%E6%B5%B4%E5%8F%A3%E4%BA%A4-%E8%B6%85%E5%88%BA%E6%BF%80/']

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
                full_url = split_joint('http://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
