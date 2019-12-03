# -*- coding: utf-8 -*-
# @Time : 2019/12/3 22:03
# @Author : wangmengmeng
import yaml
from config.config import YAML_PATH

with open(YAML_PATH + '/test.yaml', 'r', encoding='utf8') as f:
    content = yaml.load(f, Loader=yaml.FullLoader)
print(content)
# print(type(content))
# print(content.items())
# print(tuple(content.values()))

dict_all = [tuple(i.values())[1::] for i in content] # 第一个字段为接口描述，不需要取出
print(dict_all)