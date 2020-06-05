# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class findelItem(scrapy.Item):
    
    link = scrapy.Field()     #链接
    classsify = scrapy.Field()#目录路径，需要每个类别用/分开
    title = scrapy.Field() #商品标题
    code = scrapy.Field()   #商品编号
    age_range= scrapy.Field()   #商品年龄范围
