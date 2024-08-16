from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyoueight -o langyoueight.json
https://www.751mm.com/
'''


class LangyoueightSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = '751mm'
    # 后缀
    suffix = '.com/'
    name = 'langyoueight'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        pUrls = response.xpath("//video[@id='video']/@poster").extract()
        video_url = response.xpath("//video[@id='video']/@src").extract()
        tags = response.xpath("//div[@class='box clearfix f15 crumb']//a/text()").extract()
        names = response.xpath("//div[@class='box clearfix f15 crumb']/text()").extract()
        if len(video_url) and len(pUrls) and len(names) and len(tags):
            self.i = self.i + 1
            name = names[-1].strip()
            if '»' in name:
                name = name[name.index('»') + 1:].strip()
            yield get_video_item(id=self.i, tags=tags[0].strip(), url='', name=name, pUrl=pUrls[0], vUrl=video_url[0])
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
