from ScrapyObject.spiders.utils.url_utils import *

'''
进行中
scrapy crawl nc -o nc.json
https://ncao12.nccm0m1.com/index.html
https://ncao9.ncfu2qu.xyz/index.html
'''


class NcSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://ncao12.'
    # 中缀
    website = 'ncfu2qu'
    # 后缀
    suffix = '.xyz/'
    name = 'nc'
    allowed_domains = [website + '.xyz']
    start_urls = [prefix + website + suffix + 'index.html']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = get_video_url_one(content)
        pUrls = re.findall(r"\('/.*?jpg'\);", content, re.IGNORECASE)
        names = response.xpath("//h1[@class='video-title']/text()").extract()
        tags = response.xpath("//div[@class='video-detail']//p//span//a/text()").extract()
        if len(video_url) and len(pUrls) and len(names) and len(tags):
            for url in list(set(video_url)):
                self.i = self.i + 1
                yield get_video_item(id=self.i, tags=tags[0], url='', name=names[0], pUrl='https://ncdncd-sslmi.com'+pUrls[0][2:-3], vUrl='https://ncdncd-sslmi.com'+url[url.find('.com/')+4:])
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
