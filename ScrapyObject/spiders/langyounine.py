from ScrapyObject.spiders.utils.url_utils import *

'''
已失效
scrapy crawl langyounine -o langyounine.json
https://f050a63.crxzc.top/
'''


class LangyounineSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://f050a63.'
    # 中缀
    website = 'crxzc'
    # 后缀
    suffix = '.top/'
    name = 'langyounine'
    allowed_domains = [website + '.top']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl='', vUrl=format_url_one(video_url[0]))
        urls = response.xpath("//div[@class='thumbnail group']//div//a/@ href").extract()
        pUrls = response.xpath("//div[@class='thumbnail group']//div//a//img[@class='lozad w-full']/@ data-src").extract()
        names = response.xpath("//div[@class='thumbnail group']//div//a//img[@class='lozad w-full']/@ alt").extract()
        tags = response.xpath("//h1[@class='text-center text-2xl text-nord4 mb-6']/text()").extract()
        if len(urls) and len(pUrls) and len(names) and len(tags):
            for i in range(len(pUrls)):
                self.i = self.i + 1
                tag = tags[0]
                if '视频 在线看' in tag:
                    tag = tag[:tag.index('视频 在线看')].strip()
                    yield get_video_item(id=self.i, tags=tag, url=split_joint(self.prefix + self.website + self.suffix, urls[i]), name=names[i], pUrl=pUrls[i])
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
