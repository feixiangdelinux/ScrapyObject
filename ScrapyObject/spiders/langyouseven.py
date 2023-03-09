from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyouseven -o langyouseven.json
http://6613dy.com
'''


class LangyousevenSpider(scrapy.Spider):
    # 前缀
    prefix = 'http://'
    # 中缀
    website = '6613dy'
    # 后缀
    suffix = '.com/'
    name = 'langyouseven'
    allowed_domains = [website + '.com']
    start_urls = [prefix + website + suffix]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = re.findall(r'now="http.*?\.m3u8', content, re.IGNORECASE)
        if len(video_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags='', url=response.url, name='', pUrl="", vUrl=video_url[0][5:])
        p_url = response.xpath("//img[@class='img-responsive lazyload']/@ data-original").extract()
        if len(p_url):
            url = response.xpath("//a[@class='pic']/@ href").extract()
            name = response.xpath("//a[@class='pic']/@ title").extract()
            tags = response.xpath("//p[@class='data']//a/text()").extract()
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=tags[0], url=split_joint(self.prefix + self.website + self.suffix, url[0]), name=name[0], pUrl=p_url[0], vUrl='')
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and (url.endswith('.html') or url.endswith('/')):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
