# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class findelItem(scrapy.Item):
    
    classsify = scrapy.Field()#分类
    img = scrapy.Field()      #缩略图
    headline = scrapy.Field() #商品标题
    number = scrapy.Field()   #商品编号
    price = scrapy.Field()    #商品价格
    describe = scrapy.Field() #商品描述
    nature = scrapy.Field()   #商品属性（颜色）
    delivery = scrapy.Field() #商品货期
