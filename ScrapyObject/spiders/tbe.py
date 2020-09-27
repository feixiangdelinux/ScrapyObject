# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider tbe www.tbe7.com
# 运行爬虫ok
# scrapy crawl tbe -o tbe.json
class TbeSpider(scrapy.Spider):
    name = 'tbe'
    website = 'tbe7'
    allowed_domains = [website + '.com']
    # start_urls = ['http://www.tbe7.com/']
    # start_urls = ['http://tbe7.com/index.php/vod/detail/id/7831.html']
    start_urls = ['http://tbe7.com/index.php/vod/play/id/7831/sid/1/nid/1.html']
    # start_urls = ['http://tbe7.com/index.php/vod/play/id/7831/sid/2/nid/1.html']

    def __init__(self):
        global website
        self.i = 1

    def parse(self, response):
        content = get_data(response)
        pUrl = response.xpath("//div[@class='media']//img/@ src").extract()
        if len(pUrl):
            urls = response.xpath("//dt[@class='playurl2']//a/@ href").extract()
            tags = response.xpath("//div[@class='media']//dt/text()").extract()[-2][4:]
            name = response.xpath("//div[@class='media']//dt/text()").extract()[2][3:]
            for k in urls:
                item = VideoBean()
                item['id'] = self.i
                item['e'] = ''
                item['i'] = '0'
                item['name'] = name
                item['url'] = split_joint('http://' + self.website + '.com/', k)
                if len(tags):
                    item['tags'] = tags
                else:
                    item['tags'] = '综合'
                item['pUrl'] = pUrl[0]
                item['vUrl'] = ''
                self.i = self.i + 1
                yield item
        video_url = re.findall(r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',content,re.IGNORECASE)
        if len(video_url):
            item = VideoBean()
            item['id'] = self.i
            item['e'] = ''
            item['i'] = '0'
            item['name'] = ''
            item['url'] = response.url
            item['tags'] = ''
            item['pUrl'] = ''
            item['vUrl'] = format_url_one(video_url[0])
            self.i = self.i + 1
            yield item
        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
