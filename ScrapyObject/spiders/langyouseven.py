from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyouseven -o langyouseven.json
http://www.023386295.xyz:20199/
'''


class LangyousevenSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://www.'
    # 中缀
    website = '023386295'
    # 后缀
    suffix = '.xyz:20199/'
    name = 'langyouseven'
    allowed_domains = [website + '.xyz']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl="", vUrl=video_url[0])
        tags = response.xpath("//div[@class='textlink']//a/text()").extract()
        name = response.xpath("//div[@class='content clearfix']//a//img/@ alt").extract()
        p_url = response.xpath("//div[@class='content clearfix']//a//img/@ src").extract()
        url = response.xpath("//div[@class='item']//a/@ href").extract()
        if len(tags) and len(name) and len(p_url) and len(url):
            for i in range(len(url)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[-1], url=split_joint(self.prefix + self.website + self.suffix, url[i]), name=name[0], pUrl=split_joint(self.prefix + self.website + self.suffix, p_url[0]), vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
