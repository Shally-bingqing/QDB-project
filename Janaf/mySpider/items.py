# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

 #我爱卡论坛首页的爬虫数据结构
class IndexdisItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    pass
#版区帖子的爬虫数据结构
class PartissueItem(scrapy.Item):
    no = scrapy.Field()
    title = scrapy.Field()
    hot = scrapy.Field()
    time = scrapy.Field()
    link = scrapy.Field()
    pass
class Element(scrapy.Item):
    name=scrapy.Field()
    values=scrapy.Field()
    pass