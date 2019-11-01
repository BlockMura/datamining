# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


from avitoavto.items import AvitoCarList


class AvitoCarSpider(scrapy.Spider):
    name = 'avito_car'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/avtomobili?cd=1&radius=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath (
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
            yield response.follow(itm, callback=self.parse_avito_car)


    def parse_avito_car(self, response: HtmlResponse):
        item = ItemLoader(AvitoCarList(), response)
        item.add_xpath('title', '//h1[@class="title-info-title"]/span[@itemprop="name"]/text()')  #заголовок
        item.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content') #цена
        item.add_xpath('photos', '//div[contains(@class, "js-gallery-img-frame")]/@data-url') #фото
        item.add_xpath('params', '//div[@class="item-params"]/ul[@class="item-params-list"]/li/text()') #параметры
        #item.add_xpath('autoteka', '//div[@class = "autoteka-teaser-wrapper"]'#

        yield item.load_item()

