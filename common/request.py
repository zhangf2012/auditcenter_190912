# @Time : 2019/8/6 13:59
# @Author : wangmengmeng
import requests
import json
from common.login import Login
from common.logger import log
from requests import session


class HttpRequest:
    def __init__(self):
        login = Login()
        self.s = login.get_session()

    @staticmethod
    def post_xml(url, param):
        """
        不需要登录的post请求,且请求体为xml格式
        :param url:
        :param param:
        :return:
        """
        headers = {"Content-Type": "text/plain"}
        res = requests.post(url, data=param.encode("utf-8"), headers=headers)
        return res

    def post_json(self, url, param):
        data = param
        data = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        res = self.s.post(url, data=data.encode("utf-8"), headers=headers).json()
        return res

    def get(self, url):
        return self.s.get(url).json()

    def put(self, url, param):
        data = param
        data = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        return self.s.put(url, data, headers=headers)

    def req(self, url, method, data=None, params=None, headers=None):
        """封装post和get请求"""
        if method == 'post':
            return self.s.post(url=url, data=data, headers=headers)

        elif method == 'get':
            return self.s.get(url=url, params=params, headers=headers)

        else:
            return self.s.put(url=url, data=data, headers=headers)

    def http_post(self, url, json=None):
        return self.s.post(url, json=json)  # 这种封装方式只适合入参为json格式的请求，不适用于表单请求

    def http_get(self, url, params=None):
        return self.s.get(url, params=params)
