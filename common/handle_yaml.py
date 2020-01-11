# -*- coding: utf-8 -*-
# @Time : 2019/12/3 22:03
# @Author : wangmengmeng
import yaml
import os
from config.config import YAML_PATH


class HandleYaml:
    def __init__(self):
        pass

    def read_yaml(self, filename):
        with open(os.path.join(YAML_PATH, filename), 'r', encoding='utf8') as f:
            file_content = yaml.load(f, Loader=yaml.FullLoader)
        datas = [tuple(i.values())[1::] for i in file_content]
        print(file_content)
        return datas


if __name__ == '__main__':
    hy = HandleYaml()
    hy.read_yaml('test.yaml')
# print(type(content))
# print(content.items())
# print(tuple(content.values()))
#
# dict_all = [tuple(i.values())[1::] for i in content] # 第一个字段为接口描述，不需要取出
# print(dict_all)
