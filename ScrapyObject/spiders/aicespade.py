import json

from ScrapyObject.spiders.utils.url_utils import *

"""
已完成
scrapy crawl aicespade -o aicespade.json
https://fulizxc1.cc/
"""


class AicespadeSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'fulizxc1'
    # 后缀
    suffix = '.cc/'
    name = 'aicespade'
    allowed_domains = [website + '.cc']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = response.body.decode('utf-8')
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        pUrls = response.xpath("//div[@class='content']//a//img/@ src").extract()
        urls = response.xpath("//div[@class='content']//a[@target='_blank']/@ href").extract()
        names = response.xpath("//div[@class='content']//a//img/@ title").extract()
        tags = response.xpath("//div[@class='subtitle text-ellipsis']//a/@ title").extract()
        if len(urls) and len(pUrls) and len(names) and len(tags):
            for i in range(len(urls)):
                index = int(i / 2)
                self.i = self.i + 1
                pUrl = pUrls[index]
                if pUrl.startswith('/'):
                    pUrl = split_joint(self.prefix + self.website + self.suffix, pUrl)
                yield get_video_item(id=self.i, tags=tags[index], url=split_joint(self.prefix + self.website + self.suffix, urls[i]), name=names[index], pUrl=pUrl, vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
