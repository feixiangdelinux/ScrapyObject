# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider zzhmtyn http://zzhmtyn188.com
# 运行爬虫
# scrapy crawl msp -o msp.json
class MspSpider(scrapy.Spider):
    website = '7msp8'
    name = 'msp'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.' + website + '.com/']

    # start_urls = [
    #     'http://www.7msp8.com/22731/%E6%9F%90%E8%AE%BA%E5%9D%9B%E5%80%92%E9%97%AD%E5%89%8D%E8%B4%AD%E4%B9%B0%E7%9A%84%E5%BA%B7%E5%85%88%E7%94%9F%E6%9C%80%E6%96%B0%E4%BD%9C%E5%93%81%E6%9E%81%E5%93%81%E6%B0%94%E8%B4%A8%E5%AD%A6%E9%99%A2%E6%B4%BE%E7%BE%8E%E5%A5%B3%E7%A9%BF%E7%9D%80%E9%BB%91%E4%B8%9D%E8%A2%9C%E5%B9%B2%E8%BF%98%E5%BE%80%E9%B8%A1%E5%B7%B4%E6%91%B8%E6%B2%B91080p%E9%AB%98%E6%B8%85/']

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

        # # 从结果中提取所有url
        # url_list = get_url(content)
        # # 把url添加到请求队列中
        # for url in url_list:
        #     full_url = split_joint('http://www.' + self.website + '.com/', url)
        #     yield scrapy.Request(full_url, callback=self.parse)
