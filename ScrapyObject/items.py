# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyobjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VideoBean(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    e = scrapy.Field()
    i = scrapy.Field()  # isValid视频是否可以播放	0待审核	1能播	2不能播
    tags = scrapy.Field()
    pUrl = scrapy.Field()
    vUrl = scrapy.Field()

    # def __eq__(self, other):
    #     if isinstance(other, VideoBean):
    #         return self.vUrl == other.vUrl
    #     else:
    #         return False
    #
    # def __hash__(self):
    #     return hash(self.vUrl)


class VideoInfo(scrapy.Item):
    id = scrapy.Field()
    status = scrapy.Field()
    vUrl = scrapy.Field()
