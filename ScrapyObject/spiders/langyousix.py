import base64

from ScrapyObject.spiders.utils.url_utils import *

'''
已完成
scrapy crawl langyousix -o langyousix.json
https://20240819.13mei1.buzz/13mei/detail/186171103.html
'''


class LangyousixSpider(scrapy.Spider):
    # 前缀
    prefix = 'https://20240819.'
    # 中缀
    website = '13mei1'
    # 后缀
    suffix = '.buzz/'
    name = 'langyousix'
    allowed_domains = [website + '.buzz']
    start_urls = [prefix + website + suffix + '13mei/?index=index']

    def __init__(self):
        self.i = 0

    def parse(self, response):
        content = get_data(response)
        video_url = re.findall(r"var playUrl = 'http.*?\.M3U8|var playUrl = 'http.*?\.MP4|var playUrl = 'http.*?\.WMV|var playUrl = 'http.*?\.MOV|var playUrl = 'http.*?\.AVI|var playUrl = 'http.*?\.MKV|var playUrl = 'http.*?\.FLV|var playUrl = 'http.*?\.RMVB|var playUrl = 'http.*?\.3GP", content, re.IGNORECASE)
        tags = response.xpath("//div[@class='play_date']//span//script/text()").extract()
        names = response.xpath("//div[@class='play_title van-multi-ellipsis--l2 break']//script/text()").extract()
        image_url = re.findall(r'"cover":"http.*?\.jpg', content, re.IGNORECASE)
        if len(video_url) and len(tags) and len(names) and len(image_url):
            self.i = self.i + 1
            yield get_video_item(id=self.i, tags=base64.b64decode(tags[0].replace("document.write(d_d('", '').replace("'));", '')).decode('utf-8'), url='', name=base64.b64decode(names[0].replace("document.write(d_d('", '').replace("'));", '')).decode('utf-8'), pUrl=image_url[0].replace('"cover":"', ''), vUrl=video_url[0].replace("var playUrl = '", ''))
        url_list = get_url(content)
        # 提取url
        for url in url_list:
            if url.startswith('/') and url.endswith('.html'):
                yield scrapy.Request(split_joint(self.prefix + self.website + self.suffix, url), callback=self.parse)
