# -*- coding: utf-8 -*-

import re
import json
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    follow = {}
    comment_like = {}
    #pars_user = ['ms.emelia', 'realdonaldtrump']



    def __init__(self, login, pwd, pars_user, *args, **kwargs):
        self.login = login
        self.pwd = pwd
        self.pars_user_name = pars_user
        self.query_hash = 'd04b0a864b4b54837c0d870b0e77e076'
        super().__init__(*args, *kwargs)


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

        yield scrapy.FormRequest(
            inst_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pwd},
            headers={'X-CSRFToken': csrf_token}
        )

        print(1)

    def parse_users(self, response: HtmlResponse):

        for users in self.pars_user_name:
            j_body = json.loads(response.body)
            if j_body.get('authenticated'):
                yield response.follow(urljoin(self.start_urls[0], self.pars_user_name),
                                  callback=self.parse_user,
                                  cb_kwargs={'user': self.pars_user_name}
                                  )



    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars),
                              callback=self.parse_follow,
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )

    def parse_follow(self, response: HtmlResponse, user_vars, user):

        data = json.loads(response.body)
        print(1)
        if self.follow.get(user):
            self.follow[user]['edges'].extend(data['data']['user']['edge_follow']['edges'])
        else:
            self.follow[user] = {'edges': data['data']['user']['edge_follow']['edges']}
        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars)
            yield response.follow(next_page,
                                  callback=self.parse_follow,
                                  cb_kwargs={'user_vars': user_vars, 'user': user}
                                  )
            #follow = {'follow': data['data']['user']['edge_follow']['edges']}

        else:
            pass

        def parse_like_comment(self,response: HtmlResponse, user_vars, user, comment, like):  #парсим комментарии и лайки-все
            self.query_hash = 'fead941d698dc1160a298ba7bec277ac' #hash на комментарии и лайки
            page_url = self.make_graphql_url(user_vars)  # url пользователя
            for itm in page_url:
                data = json.loads(response.body)
                print(1)

                if self.follow.get(comment):
                    self.follow[comment]['edges'].extend(data['edge_media_preview_comment']['edges']['owner'])
                    self.follow[like]['edges'].extend(data)














    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        """Используя регулярные выражения парсит переданную строку на наличие
        `csrf_token` и возвращет его."""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def make_graphql_url(self, user_vars):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=self.query_hash,
            variables=urlencode(user_vars)
        )
        return result




