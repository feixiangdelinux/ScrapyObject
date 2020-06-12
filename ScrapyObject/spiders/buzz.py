# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫gan
# scrapy genspider gan www.734gan.com
# 运行爬虫ok
# scrapy crawl buzz -o buzz.json
class BuzzSpider(scrapy.Spider):
    name = 'buzz'
    website = '8144051'
    allowed_domains = ['www.' + website + '.buzz']
    start_urls = ['http://www.' + website + '.buzz/']

    # start_urls = ['http://www.3520625.buzz/html/crdongman/']

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
            title_prefix = response.xpath('/html/head/title/text()').extract()[0]
            print(title_prefix)
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
            tag = response.xpath("//li[@class='n1']//b/text()").extract()
            name = response.xpath("//div[@class='post']//a/@ title").extract()
            url = response.xpath("//div[@class='post']//a/@ href").extract()
            pUrl = response.xpath("//div[@class='post']//a//img/@ src").extract()
            if len(pUrl):
                for k in pUrl:
                    id_list = pUrl.index(k)
                    item = VideoBean()
                    item['id'] = self.i
                    item['e'] = ''
                    item['i'] = '0'
                    item['name'] = name[id_list]
                    item['url'] = split_joint('http://www.' + self.website + '.buzz/', url[id_list])
                    if len(tag):
                        item['tags'] = tag[0]
                    else:
                        item['tags'] = '综合'
                    item['pUrl'] = pUrl[id_list]
                    item['vUrl'] = ''
                    self.i = self.i + 1
                    yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css'):
                full_url = split_joint('http://www.' + self.website + '.buzz/', url)
                print(full_url)
                yield scrapy.Request(full_url, callback=self.parse)
