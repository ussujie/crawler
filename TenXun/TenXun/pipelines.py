# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
class TenxunPipeline(object):

    def __init__(self):
        #连接数据库
        self.client = pymongo.MongoClient('localhost')
        #创建数据库
        self.db = self.client['tenxun']
        #创建集合
        self.table = self.db['tenxundata']

    def process_item(self, item, spider):
        self.table.insert(dict(item))

        return item


        # fp = open('tenxun.json','a',encoding='utf-8')
        # json.dump(dict(item),fp,ensure_ascii=False)
        # return item
