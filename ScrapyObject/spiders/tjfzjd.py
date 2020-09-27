# -*- coding: utf-8 -*-
from ScrapyObject.items import VideoBean
from ScrapyObject.spiders.utils.url_utils import *


# 创建爬虫
# scrapy genspider tjfzjd www.tjfzjd.com
# 运行爬虫
# scrapy crawl tjfzjd -o tjfzjd.json
# ok
class TjfzjdSpider(scrapy.Spider):
    name = 'tjfzjd'
    website = 'tjfzjd'
    allowed_domains = ['www.' + website + '.com']
    start_urls = ['http://www.tjfzjd.com/']
    # start_urls = ['http://www.tjfzjd.com/index.php/vod/type/id/3/page/5.html']
    # start_urls = ['http://www.tjfzjd.com/index.php/vod/type/id/1/page/2.html']
    # start_urls = ['http://www.tjfzjd.com/index.php/vod/play/id/133541/sid/1/nid/1.html']

    def __init__(self):
        global website
        self.i = 1


    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(
            r'http.*?\.M3U8|http.*?\.MP4|http.*?\.WMV|http.*?\.MOV|http.*?\.AVI|http.*?\.MKV|http.*?\.FLV|http.*?\.RMVB|http.*?\.3GP',
            content, re.IGNORECASE)
        if len(video_url):
            if '\\' in video_url[0]:
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
        tags = response.xpath("//div[@class='title']//h1/text()").extract()
        if len(tags):
            if '搜索的影片' not in tags[0]:
                name = response.xpath("//a[@class='cover']//img/@ alt").extract()
                pUrl = response.xpath("//a[@class='cover']//img/@ src").extract()
                url = response.xpath("//a[@class='cover']/@ href").extract()
                for k in pUrl:
                    id_list = pUrl.index(k)
                    item = VideoBean()
                    item['id'] = self.i
                    item['e'] = ''
                    item['i'] = '0'
                    item['name'] = name[id_list]
                    item['url'] = split_joint('http://www.' + self.website + '.com/', url[id_list])
                    item['tags'] = tags[0]
                    item['pUrl'] = split_joint('http://www.' + self.website + '.com/', k)
                    item['vUrl'] = ''
                    self.i = self.i + 1
                    yield item

        # 从结果中提取所有url
        url_list = get_url(content)
        # 把url添加到请求队列中
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                full_url = split_joint('http://www.' + self.website + '.com/', url)
                yield scrapy.Request(full_url, callback=self.parse)
            elif url.startswith('http') or url.startswith('www'):
                yield scrapy.Request(url, callback=self.parse)
