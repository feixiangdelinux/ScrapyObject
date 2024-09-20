from ScrapyObject.spiders.utils.url_utils import *

'''
已失效
scrapy crawl lnalbumqqo -o lnalbumqqo.json
https://179na.com/
'''


class LnalbumqqoSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://'
    # 中缀
    website = '179na'
    # 后缀
    suffix = '.com/'
    name = "lnalbumqqo"
    allowed_domains = [website + '.com']
    # start_urls = [prefix + website + suffix]
    start_urls = ['https://179na.com/179na-movie/toupaizipai/index_2/']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        # 获取字符串类型的网页内容
        content = get_data(response)
        video_url = re.findall(r'source:.*?\.M3U8|source:.*?\.MP4|source:.*?\.WMV|source:.*?\.MOV|source:.*?\.AVI|source:.*?\.MKV|source:.*?\.FLV|source:.*?\.RMVB|source:.*?\.3GP', content, re.IGNORECASE)
        if len(video_url):
            self.i = self.i + 1
            vsdfasd = ''
            if 'https://' in video_url[0]:
                vsdfasd = video_url[0].replace('source: \'', '')
            else:
                vsdfasd = video_url[0].replace('source: \'', 'https:')
            yield get_video_item(id=self.i, url=response.url, vUrl=vsdfasd)
        else:
            img_list = response.xpath("//div[@class='video-elem']//a[@class='display d-block']//div[@class='img']/@style").extract()
            url_list = response.xpath("//div[@class='video-elem']//a[@class='title text-sub-title mt-2 mb-3']/@href").extract()
            name_list = response.xpath("//div[@class='video-elem']//a[@class='title text-sub-title mt-2 mb-3']/text()").extract()
            tag_list = response.xpath('/html/head/title/text()').extract()
            if len(img_list) and len(url_list) and len(name_list) and (len(tag_list) and '-' in tag_list[0]):
                for index in range(len(img_list)):
                    self.i = self.i + 1
                    picture_url = 'https:' + re.findall(r"background-image:.*?url\((.*?)'\)", img_list[index], re.IGNORECASE)[0].replace('\'', '')
                    picture_url = picture_url.replace('https://img5.aiaixx.top/', 'https://img5.biqugecn.cc/')
                    tag = tag_list[0][:tag_list[0].index('-')].strip()
                    yield get_video_item(id=self.i, tags=tag, url=split_joint(self.prefix + self.website + self.suffix, url_list[index]), name=name_list[index], pUrl=picture_url)
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)