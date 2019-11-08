# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient

class HeadhuntPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://Localhost:27017'
        client = MongoClient(mongo_url)
        hh_bd = client.headhunt
        self.hh_collec = hh_bd.hh_vac
    def process_item(self, item, spider):
        self.hh_collec.insert_one(item)
        return item