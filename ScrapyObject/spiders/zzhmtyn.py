# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider zzhmtyn http://zzhmtyn188.com
# 运行爬虫
# scrapy crawl zzhmtyn -o zzhmtyn.json
class ZzhmtynSpider(scrapy.Spider):
    name = 'zzhmtyn'
    website = 'zzhmtyn188'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.' + website + '.com/']

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
            if "-" in title_prefix:
                item['name'] = title_prefix[:title_prefix.index("-")]
            else:
                item['name'] = title_prefix
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[-1]
            self.i = self.i + 1
            yield item
        else:
            pUrl = response.xpath("//img[@class='pic l']/@ src").extract()
            if len(pUrl):
                url = response.xpath("//a[@title='第1集']/@ href").extract()[0]
                print(url)
                name = response.xpath("//img[@class='pic l']/@ alt").extract()[0]
                tags = response.xpath("//a[@target='_blank']/text()").extract()[0]
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name
                item['url'] = 'http://www.' + self.website + '.com' + url
                item['tags'] = tags
                item['pUrl'] = pUrl[0]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item

        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            full_url = split_joint('http://www.' + self.website + '.com/', url)
            yield scrapy.Request(full_url, callback=self.parse)
