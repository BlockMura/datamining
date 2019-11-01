# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class HhVacSpider(scrapy.Spider):
    name = 'hh_vac'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=экономист&page=0']

    def parse(self, response: HtmlResponse ):
        pagination = response.css('a.bloko-button.HH-Pager-Control::attr(href)').extract()
        next_link = pagination[-1]
        yield response.follow(next_link, callback=self.parse)
        print(response.url)

        vac_url = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for itm in vac_url:
            yield response.follow(itm, callback=self.parce_page_vac)


        def parse_page_vac(self, response: HtmlResponse):
            title = response.css('a.bloko-link.HH-LinkModifier::text').extract_first() #название вакансии
            hh_url = response.css('a.bloko-link.bloko-link_secondary.HH-AnonymousIndexAnalytics-Recommended-Company::attr(href)').extract_first() # ссылкм на страницу в HH
            name_company = response.css('a.bloko-link.bloko-link_secondary.HH-AnonymousIndexAnalytics-Recommended-Company::text').extract_first() #название компании
            compens = response.css('div.vacancy-serp-item__compensation::text').extract_first() # ЗП

            yield {'title': title,
                   'hh_url' : hh_url,
                   'name_company' : name_company,
                   'compens' : compens,
            }











