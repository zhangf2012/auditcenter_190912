# -*- coding: utf-8 -*-
# @Time : 2019/12/3 22:03
# @Author : wangmengmeng
import os

host='10.1.1.120'
port=22
username='yyuser'
password='iPh@Yyuse2'

auditcennter_url = "http://10.1.1.120:9999/auditcenter"
PROJ_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_PATH = os.path.join(PROJ_PATH,'yamlfiles')

if __name__ == '__main__':
    print(PROJ_PATH)
