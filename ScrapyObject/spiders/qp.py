# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫gan
# scrapy genspider qp www.q22p.cc
# 运行爬虫ok
# scrapy crawl qp -o qp.json
# 没问题
# http://www.q22p.cc/index.php/vod/play/id/233652/sid/1/nid/1.html
# qp
class QpSpider(scrapy.Spider):
    name = 'qp'
    website = 'q22p'
    allowed_domains = ['www.' + website + '.cc']
    start_urls = ['http://www.q22p.cc/']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//div[@class='detail-pic fn-left']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//div[@class='video_list fn-clear']//a/@ href").extract()
            tags = response.xpath("//ul[@class='bread-crumbs']//li//a/text()").extract()[-2]
            name = response.xpath("//div[@class='detail-title fn-clear']//h1/text()").extract()[0]
            for k in urls:
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name
                item['url'] = split_joint('http://www.' + self.website + '.cc/', k)
                if len(tags):
                    item['tags'] = tags
                else:
                    item['tags'] = '综合'
                item['pUrl'] = split_joint('http://www.' + self.website + '.cc/', pUrl[0])
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        video_url = re.findall(
            r'http.*?M3U8|http.*MP4|http.*WMV|http.*MOV|http.*AVI|http.*MKV|http.*FLV|http.*RMVB|http.*3GP', content,
            re.IGNORECASE)
        if len(video_url):
            name = response.xpath("//ul[@class='bread-crumbs']//li/text()").extract()[0]
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = name[:-6]
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[0].replace("\\/", "/")
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css') and 'javascript' not in url:
                full_url = split_joint('http://www.' + self.website + '.cc/', url)
                yield scrapy.Request(full_url, callback=self.parse)
