# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class findelItem(scrapy.Item):
    
    link = scrapy.Field()     #链接
    classsify = scrapy.Field()#目录路径，需要每个类别用/分开
    img = scrapy.Field()      #缩略图
    img_clear = scrapy.Field()#清晰图 
    title = scrapy.Field() #商品标题
    code = scrapy.Field()   #商品编号
    price = scrapy.Field()    #商品价格
    describe = scrapy.Field() #商品描述 (需要进入页面)
    nature = scrapy.Field()   #商品属性（颜色）(需要进入页面)
    delivery = scrapy.Field() #商品货期 (需要进入页面)
