# -*- coding: utf-8 -*-
# @Time : 2019/12/3 22:03
# @Author : wangmengmeng
import os

PROJ_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_PATH = os.path.join(PROJ_PATH,'yamlfiles')

if __name__ == '__main__':
    print(PROJ_PATH)
