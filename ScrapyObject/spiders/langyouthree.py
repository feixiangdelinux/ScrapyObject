from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyouthree -o langyouthree.json
https://www.tangxinshipin.live/
'''


class LangyouthreeSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://www.'
    # 中缀
    website = 'tangxinshipin'
    # 后缀
    suffix = '.live/'
    name = 'langyouthree'
    allowed_domains = [website + '.live']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = get_video_url_one(content)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, url=response.url, vUrl=format_url_one(video_url[0]))
        url = response.xpath("//div[@class='detail-poster']//a/@ href").extract()
        p_url = response.xpath("//div[@class='detail-poster']//a//img/@ src").extract()
        name = response.xpath("//div[@class='detail-poster']//a//img/@ alt").extract()
        if len(name) and len(p_url) and len(url):
            tags = response.xpath("//meta[@name='keywords']/@ content").extract()[0]
            if '_糖心部落' in tags:
                tags = tags[:tags.find("_糖心部落")].strip()
            if name[0] in tags:
                tags = tags[:tags.find(name[0])].strip()
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags, url=split_joint(self.prefix + self.website + self.suffix, url[0]), name=name[0], pUrl=p_url[0])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.strip().startswith('/') and url.strip().endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)