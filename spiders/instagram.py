import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'anzhelo4ka'
    insta_pwd = ' '
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    graphql_url = 'https://www.instagram.com/graphql/query/'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def __init__(self, friends):
        self.parse_users = friends

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.authorization,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token})

    def authorization(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                        f'/{user}',
                        callback=self.user_parse,
                        cb_kwargs={'username': user})

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
               'id': user_id,
                'include_reel': True,
                'fetch_mutual': True,
                'first': 24}
        followers_url = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
        yield response.follow(
            followers_url,
            callback=self.followers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)})
        following_url = f'{self.graphql_url}query_hash={self.following_hash }&{urlencode(variables)}'
        yield response.follow(
            following_url,
            callback=self.following_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)})

    def followers_parse(self, response: HtmlResponse, user_id, username, variables):
        f_j= json.loads(response.text)
        page_info =f_j.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            followers_url = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                    followers_url ,
                    callback=self.followers_parse,
                    cb_kwargs={'user_id': user_id,
                               'username': username,
                               'variables': deepcopy(variables)})

            followers = f_j.get('data').get('user').get('edge_followed_by').get('edges')
            for follower in followers:
                info = InstaparserItem(
                    id=user_id,
                    name=username,
                    user_id=follower['node']['id'],
                    user_name=follower['node']['username'],
                    user_fullname=follower['node']['full_name'],
                    photo=follower['node']['profile_pic_url'],
                    type='follower')
                yield info

    def following_parse(self, response: HtmlResponse, user_id, username, variables):
        f_j = json.loads(response.text)
        page_info = f_j.get('data').get('user').get('edge_follow').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            following_url = f'{self.graphql_url}query_hash={self.following_hash }&{urlencode(variables)}'
            yield response.follow(
                following_url,
                    callback=self.following_parse,
                    cb_kwargs={'user_id': user_id,
                               'username': username,
                               'variables': deepcopy(variables)})

            followings = f_j.get('data').get('user').get('edge_follow').get('edges')
            for following in followings:
                info = InstaparserItem(
                    id=user_id,
                    name=username,
                    user_id=following['node']['id'],
                    user_name=following['node']['username'],
                    user_fullname=following['node']['full_name'],
                    photo=following['node']['profile_pic_url'],
                    type='following')
                yield info

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')



