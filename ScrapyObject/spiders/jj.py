# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# scrapy startproject ScrapyObject
# 创建爬虫
# scrapy genspider msp www.c777j.com
# 运行爬虫ok
# scrapy crawl jj -o jj.json
# 没问题
class JjSpider(scrapy.Spider):
    name = 'jj'
    website = 's888r'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['https://www.' + website + '.com/']

    # start_urls = ['https://www.p888v.com/vod/html9/html22/36459.html']
    # start_urls = ['https://www.s888r.com/vod/html1/', 'https://www.s888r.com/vod/html1/',
    #               'https://www.s888r.com/vod/html9/', 'https://www.s888r.com/vod/html16/',
    #               'https://www.s888r.com/vod/html17/', 'https://www.s888r.com/vod/html26/index_2.html',
    #               'https://www.s888r.com/vod/html27/',]

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
                item['pUrl'] = k
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html'):
                if url.startswith('/'):
                    full_url = split_joint('https://www.' + self.website + '.com/', url)
                    yield scrapy.Request(full_url, callback=self.parse)
                else:
                    yield scrapy.Request(url, callback=self.parse)
