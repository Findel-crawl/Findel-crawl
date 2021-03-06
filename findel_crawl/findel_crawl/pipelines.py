# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FindelCrawlPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri  #定义实例变量mongo_uri和mongo_db
        self.mongo_db = mongo_db

    @classmethod
    
    #这个类方法就是为了使用crawler来获取全局settings中的MONGO_URI和MONGO_DB的值，并复制给mongo_uri和mongo_db
    
    def from_crawler(cls,crawler):   
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'), 
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)  #与数据库建立连接
        self.db = self.client[self.mongo_db] #打开数据库

    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].update({'code': item['code']},{'$set': dict(item)}, True)
        return item  #这个item返回才能被其他的中间件获取
            
    def close_spider(self,spider):
        self.client.close()  #关闭数据库连接

