# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *
# 创建爬虫
# scrapy genspider zx www.zx9000.com
# 运行爬虫ok
# scrapy crawl zx -o zx.json
class ZxSpider(scrapy.Spider):
    name = 'zx'
    website = 'zx9000'
    # allowed_domains = ['http://' + website + '.com']
    allowed_domains = ['zx9000.com']
    start_urls = ['http://zx9000.com']

    # start_urls = ['http://zx9000.com/?m=vod-play-id-3228-src-2-num-1.html']
    # start_urls = ['http://zx9000.com/?m=vod-type-id-8.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r'https.*?\.m3u8', content, re.IGNORECASE)
        if len(video_url):
            tag = response.xpath("//span[@class='cat_pos_l']//a/text()").extract()
            print(tag)
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['url'] = response.url
            item['vUrl'] = video_url[0][video_url[0].rfind('https'):]
            item['name'] = tag[-1]
            item['tags'] = tag[-2]
            item['pUrl'] = ''
            self.i = self.i + 1
            yield item
        pUrl = response.xpath("//div[@class='box movie_list']//ul//li//a//img/@ src").extract()
        if len(pUrl):
            url = response.xpath("//div[@class='box movie_list']//ul//li//a/@ href").extract()
            name = response.xpath("//div[@class='box movie_list']//ul//li//a//h3/text()").extract()
            for k in pUrl:
                position = pUrl.index(k)
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name[position]
                item['url'] = split_joint('http://' + self.website + '.com/', url[position])
                item['tags'] = ''
                if '#' in pUrl[position]:
                    item['pUrl'] = pUrl[0][:pUrl[0].rfind('#')]
                else:
                    item['pUrl'] = pUrl[position]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://zx9000.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)