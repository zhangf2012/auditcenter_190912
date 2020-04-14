# -*- coding: utf-8 -*-
# @Time : 2020/3/5 22:15
# @Author : wangmengmeng
import paramiko
from config.config import host, port, username, password
import time
import datetime
import xmltodict
from pprint import pprint
curdate = ((datetime.datetime.now())).strftime("%Y-%m-%d")  # 获取当天日期
print(curdate)


class ConLinux:

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, username, password)

    def get_client(self):
        # ['root']['orders']['herb_medical_order']['herb_medical_order_info']['order_status']
        # pid = '1586844369460'
        # stdout = self.client.exec_command('cat /tmp/hisresult/{}/H0003/return_path/{}*.txt'.format(curdate, pid))[1]
        # content = stdout.read()
        # print(content.decode('utf-8'))
        # print(type(content))
        # pprint(content.decode('utf-8'))
        return self.client
if __name__ == '__main__':
    cl = ConLinux()
    cl.get_client()