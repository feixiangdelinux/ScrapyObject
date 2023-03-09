from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyounine -o langyounine.json
http://6222dy.com
'''


class LangyounineSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '6222dy'
    # 后缀
    suffix = '.com/'
    name = 'langyounine'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix + 'index.php']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = re.findall(r'now="http.*?\.m3u8', content, re.IGNORECASE)
        name = response.xpath("//span[@class='vod_history hide']/@data-name").extract()
        p_url = response.xpath("//span[@class='vod_history hide']/@data-pic").extract()
        tag = response.xpath("//div[@class='text-muted']/text()").extract()
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tag[-1].strip()[:tag[-1].strip().index(' /')], url='', name=name[0], pUrl=p_url[0], vUrl=video_url[0][5:])
        url_list = get_url(content)
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
