# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# scrapy startproject ScrapyObject
# 创建爬虫
# scrapy genspider msp www.7msp8.com
# 运行爬虫
# scrapy crawl jj -o jj.json
class JjSpider(scrapy.Spider):
    name = 'jj'
    website = '2678mo'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/']

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
            title_prefix = title_prefix.replace(" ", "")
            if "-下载地址" in title_prefix:
                item['name'] = title_prefix[:title_prefix.index("-下载地址")]
            else:
                item['name'] = title_prefix
            item['url'] = split_joint('https://www.' + self.website + '.com/',
                                      response.xpath("//li[@id='nav-index']/a/@ href").extract()[-1])
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = video_url[-1]
            self.i = self.i + 1
            yield item

        pUrl = response.xpath("//a[@class='video-pic loading']/@ data-original").extract()
        url = response.xpath("//a[@class='video-pic loading']/@ href").extract()
        name = response.xpath("//h5[@class='text-overflow']/a[@target='_blank']/text()").extract()
        types = response.xpath("//a[@data='order-addtime']/text()").extract()
        if len(pUrl):
            for k in pUrl:
                id_list = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['name'] = name[id_list].replace(" ", "")
                item['url'] = split_joint('https://www.' + self.website + '.com/', url[id_list])
                item['e'] = ""
                item['i'] = '0'
                if len(types):
                    item['tags'] = types[0]
                else:
                    item['tags'] = "综合"
                if len(k):
                    item['pUrl'] = k
                else:
                    item['pUrl'] = "https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike92%2C5%2C5" \
                                   "%2C92%2C30/sign=425563eef436afc31a013737d27080a1" \
                                   "/3bf33a87e950352a87460b265043fbf2b2118bfc.jpg "
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if not url.endswith('.css'):
                full_url = split_joint('https://www.' + self.website + '.com/', url)
                print(full_url)
                yield scrapy.Request(full_url, callback=self.parse)
