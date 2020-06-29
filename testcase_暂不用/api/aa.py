# -*- coding: utf-8 -*-
# @Time : 2019/12/4 22:24
# @Author : wangmengmeng
from common.request import HttpRequest
from common.handle_yaml import HandleYaml

requ = HttpRequest()
hy = HandleYaml()
datas = hy.read_yaml('auditcenter.yaml')
print(datas)