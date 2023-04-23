# -*- coding: utf-8 -*-
from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl ck -o ck.json
http://ckv8.cc/
'''


class CkSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://'
    # 中缀
    website = 'ckv8'
    # 后缀
    suffix = '.cc/'
    name = 'ck'
    allowed_domains = [website + '.cc']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        soup = BeautifulSoup(content, 'html.parser')  # 文档对象
        info = soup.find_all('h3', class_='title')
        if len(info) == 2:
            tag = info[-1].text[0:15].strip()
            for k in soup.find_all('a'):
                if (type(k.get('title')) == str) and (type(k.get('data-original')) == str):
                    self.i = self.i + 1
                    yield get_video_item(id=self.i, name=k.get('title'), tags=tag,
                                         url=split_joint(self.prefix + self.website + self.suffix, k.get('href')),
                                         pUrl=k.get('data-original'))
        video_url_one = response.xpath("//div[@class='stui-player__video clearfix']//script/text()").extract()
        if len(video_url_one):
            temp_url_one = video_url_one[0][video_url_one[0].index("http"):-1]
            temp_url_two = temp_url_one[0:temp_url_one.index("\"")]
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=format_url_one(temp_url_two))
        # 从网页中提取url链接
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.endswith('.html') and url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
