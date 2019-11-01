# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from geekbrain.items import AvitoRealEstate


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[contains(@class, "pagination")]/'
            'div[contains(@class, "pagination-nav")]/'
            'a[contains(@class, "js-pagination-next")]/@href'
        ).extract_first()
        yield response.follow(next_page, callback=self.parse)

        ads = response.xpath(
            '//div[contains(@class, "catalog_table")]'
            '//div[contains(@class, "item")]'
            '//h3[@data-marker="item-title"]/a/@href'
        ).extract()

        for itm in ads:
            yield response.follow(itm, callback=self.real_estate_parse)

    def real_estate_parse(self, response: HtmlResponse):
        item = ItemLoader(AvitoRealEstate(), response)
        item.add_xpath('title', '//h1[@class="title-info-title"]/span[@itemprop="name"]/text()')
        item.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content')
        item.add_xpath('photos', '//div[contains(@class, "js-gallery-img-frame")]/@data-url')
        item.add_xpath('params', '//div[@class="item-params"]/ul[@class="item-params-list"]/li')

        yield item.load_item()
