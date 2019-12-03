# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 16:34
# @Author  : wangmengmeng

import requests
import json
from config.read_config import ReadConfig
import hashlib
from common.logger import Logger

class Login():
    def __init__(self):
        self.conf = ReadConfig()
        url = self.conf.get('login', 'address') + '/syscenter/api/v1/currentUser'
        username = self.conf.get('login','username')
        passwd = self.conf.get('login','password')
        m = hashlib.md5() # 创建md5对象
        m.update(passwd.encode()) #  生成加密字符串
        password = m.hexdigest()
        params = {"name": username, "password": password}
        headers = {'Content-Type': "application/json"}
        self.session = requests.session()
        # res = self.session.post(url, data=json.dumps(params), headers=headers)
        res = self.session.post(url, data=json.dumps(params), headers=headers)
        print(res.json())
        start_sf_url = self.conf.get('login', 'address') + '/auditcenter/api/v1/startAuditWork'  # 获取开始审方url
        res2 = self.session.get(url=start_sf_url)  # 开始审方
        print(res2.json())

    def get_session(self):
        return self.session


if __name__ == '__main__':
    a = Login()
    # res = a.get_session()
    # print(res)
