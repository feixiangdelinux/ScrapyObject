from ScrapyObject.spiders.utils.url_utils import *

'''
网站需要翻墙
scrapy crawl langyounine -o langyounine.json
https://jinbai.milf000.icu/
'''


class LangyounineSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://jinbai.'
    # 中缀
    website = 'milf000'
    # 后缀
    suffix = '.icu/'
    name = 'langyounine'
    allowed_domains = [website + '.icu']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        url_list = response.xpath("//li//a[@class='thumbnail']/@ href").extract()
        img_list = response.xpath("//li//a[@class='thumbnail']//img/@ src").extract()
        name_list = response.xpath("//li//a[@class='thumbnail']//img/@ alt").extract()
        tag_list = response.xpath("//div[@class='breadcrumbs']//a/text()").extract()
        if len(url_list) and len(img_list) and len(name_list):
            for i in range(len(url_list)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, url=split_joint(self.prefix + self.website + self.suffix, url_list[i]), name=name_list[i], pUrl=img_list[i])
        if len(tag_list) and len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, tags=tag_list[-1], vUrl=format_url_one(video_url[0]))
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)