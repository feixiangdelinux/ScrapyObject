import json

from ScrapyObject.spiders.utils.url_utils import *

"""
这个网站不行,待重修
scrapy crawl aicespade -o aicespade.json
https://aicespade23.top/
"""


class AicespadeSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'aicespade23'
    # 后缀
    suffix = '.top/'
    name = 'aicespade'
    allowed_domains = [website + '.top']
    start_urls = [prefix + website + suffix]

    # start_urls = ['https://aicespade23.top/video_search/paco/174/index.html']
    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = response.body.decode('utf-8')
        video_url = get_video_url_one(content)
        if len(video_url):
            p_url = response.xpath("//iframe[@id='play']/@ style").extract()
            if len(p_url):
                name = response.xpath("//div[@class='textlink fn-left']//a/text()").extract()
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=name[0], url='', name=name[1], pUrl=p_url[0][p_url[0].find('(') + 1:p_url[0].find(')')], vUrl=video_url[0])
        url_list = re.findall(r'var pop.*?];', content, re.IGNORECASE)
        if len(url_list):
            datat = json.loads(url_list[0][8:-1])
            for url_list in datat:
                if len(url_list) == 6:
                    if url_list[1].startswith('/') and url_list[1].endswith('.html'):
                        yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url_list[1]), callback=self.parse)
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
