from ScrapyObject.spiders.utils.url_utils import *

'''
已失效
scrapy crawl lnalbumqqo -o lnalbumqqo.json
https://lnalbumqqo.xyz:16888/index.html
'''


class LnalbumqqoSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = 'lnalbumqqo'
    # 后缀
    suffix = '.xyz:16888/'
    name = "lnalbumqqo"
    allowed_domains = [website + '.xyz:16888']
    start_urls = [prefix + website + suffix + 'index.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=video_url[0])
        tags = response.xpath("//div[@class='title']//h1//a/text()").extract()
        urls = response.xpath("//div[@class='listpic']//a/@href").extract()
        pUrls = response.xpath("//div[@class='listpic']//a//div/@data-original").extract()
        names = response.xpath("//div[@class='vodname']/text()").extract()
        if len(tags) and len(urls) and len(pUrls) and len(names):
            for index in range(len(urls)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[-1], url=split_joint(self.prefix + self.website + self.suffix, urls[index]), name=names[index], pUrl=pUrls[index], vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
