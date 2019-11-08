# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class GbBlog2Spider(scrapy.Spider):
    name = 'gb_blog2'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['https://geekbrains.ru/posts']

    def parse(self, response: HtmlResponse):
        pagination = response.xpath(
            '//ul[contains(@class, "gb__pagination")]/li[@class="page"]/a[@rel="next"]/@href'
        ).extract_first()

        yield response.follow(pagination, callback=self.parse)

        blog_pages = response.xpath('//a[contains(@class, "post-item__title")]/@href').extract()
        for itm in blog_pages:
            yield response.follow(itm, callback=self.parse_blog_page)

    def parse_blog_page(self, response: HtmlResponse):
        title = response.xpath(
            '//article[contains(@class, "blogpost__article-wrapper")]/h1[contains(@class, "blogpost-title")]/text()'
        ).extract_first()

        image = response.xpath(
            '//article[contains(@class, "blogpost__article-wrapper")]/div[@itemprop="image"]/text()'
        ).extract_first()

        autor = response.xpath('//div[@itemprop="author"]/../@href').extract_first()
        tag_keywords = response.xpath('//i[contains(@class,"i-tag")]/@keywords').extract_first()
        tags = []
        if tag_keywords:
            tag_attr_url = '/posts?tag='
            tags = [{'name': itm, 'url': f'{tag_attr_url}itm'} for itm
                    in tag_keywords.split(', ')]

        item = {'title': title,
                'post_url': response.url,
                'image': image,
                'autor_url': autor,
                'tags': tags,
                }

        yield response.follow(autor, callback=self.creator_parse, cb_kwargs={'item': item})

    def creator_parse(self, response: HtmlResponse, item):
        item['autor_name'] = response.xpath(
            "//section[@id='main-content']//span[@class='h2']/text()"
        ).extract_first()

        item['autor_age'] = response.xpath(
            "//section[@id='main-content']//span[@class='h5']/span/text()"
        ).extract_first()
        yield item
