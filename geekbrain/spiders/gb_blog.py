# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class GbBlogSpider(scrapy.Spider):
    name = 'gb_blog'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['http://geekbrains.ru/posts']

    def parse(self, response: HtmlResponse):
        pagination = response.css('ul.gb__pagination li.page a::attr(href)').extract()
        next_link = pagination[-1]
        yield response.follow(next_link, callback=self.parse)
        print(response.url)

        blog_page = response.css('div.post-items-wrapper a.post-item__title::attr(href)').extract()
        for itm in blog_page:
            yield response.follow(itm, callback=self.parce_blog_page)


    def parce_blog_page(self, response: HtmlResponse):
        title = response.css('h1.blogpost-title::text').extract_first()
        img = response.css('div.blogpost-content img::attr(src)').extract_first()
        author = response.css('div.row.m-t div.col-md-5 a::attr(href)').extract()









#Примеры запросов на экстракт
#response.css('.page').extract()
#response.css('li.page').extract()
#response.css('ul.gb__pagination').extract()
#response.css('ul.gb__pagination li').extract()
#response.css('ul.gb__pagination li.page a').extract()
#response.css('ul.gb__pagination li.page a::attr(href)').extract() - получение ссылки
#response.css('ul.gb__pagination li.page a').attrib - вывод атрибутов тега
#response.url куда заходит пасер страниц
#response.css('h1.blogpost-title::text')
#response.css('h1.blogpost-title::text').extract_first() - вывод заголовка
#response.css('div.blogpost-content img::attr(src)').extract_first() - вывод ссылки на первое изображение
#response.css('div.row.m-t')
#response.css('div.row.m-t div.col-md-5 a::attr(href)').extract() - вывод ссылки на автора статьи


#Примеры запросов на экстракт
#response.css('.page').extract()
#response.css('li.page').extract()
#response.css('ul.gb__pagination').extract()
#response.css('ul.gb__pagination li').extract()
#response.css('ul.gb__pagination li.page a').extract()
#response.css('ul.gb__pagination li.page a::attr(href)').extract() - получение ссылки
#response.css('ul.gb__pagination li.page a').attrib - вывод атрибутов тега
#response.url куда заходит пасер страниц
#response.css('h1.blogpost-title::text')
#response.css('h1.blogpost-title::text').extract_first() - вывод заголовка
#response.css('div.blogpost-content img::attr(src)').extract_first() - вывод ссылки на первое изображение
#response.css('div.row.m-t')
#response.css('div.row.m-t div.col-md-5 a::attr(href)').extract() - вывод ссылки на автора статьи

#response.css('div.bloko-gap.bloko-gap_top').extract()
#esponse.css('div.pager-block').extract()
#response.css('div.bloko-gap bloko-gap_top').extract()
#response.css('a.bloko-button.HH-Pager-Control::attr(href)').extract() - пагинатор

#response.css('span.bloko-button-group a.bloko-button.HH-Pager-Control::attr(href)').extract()
#pagination = response.css('span.bloko-button-group span.pager-item-not-in-short-range a.bloko-button.HH-Pager-Control::attr(href)').extract()
#next_link = pagination[1]

# title =
# hh_company = {'name' : , 'hh_url'}
# url_company =
# skills =
# money =
