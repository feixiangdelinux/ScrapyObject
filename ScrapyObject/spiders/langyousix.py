from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyousix -o langyousix.json
http://www.7uun.com/
'''


class LangyousixSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '7uun'
    # 后缀
    suffix = '.com/'
    name = 'langyousix'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]


    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=format_url_one(video_url[0]))
        tags = response.xpath("//ul[@class='detail-actor clearfix']//li/text()").extract()
        urls = response.xpath("//div[@class='detail-poster']//a/@ href").extract()
        pUrls = response.xpath("//div[@class='detail-poster']//a//img/@ src").extract()
        names = response.xpath("//div[@class='detail-poster']//a//img/@ alt").extract()
        if len(urls) and len(pUrls) and len(names) and len(tags):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[1], url=split_joint(self.prefix + self.website + self.suffix, urls[0]), name=names[0], pUrl=pUrls[0], vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
