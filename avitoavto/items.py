# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def cleaner_params(item):
    result = item.split('">')[-1].split(':')
    key = result[0]
    value = result[-1].split('</span>')[-1].split('</')[0][:-1]
    return {key: value}


def dict_params(items):
    result = {}
    for itm in items:
        result.update(itm)
    return result


class AvitoavtoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AvitoCarList(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(cleaner_params), output_processor=dict_params)
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))