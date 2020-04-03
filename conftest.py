# -*- coding: utf-8 -*-
# @Time : 2020/4/3 13:45
# @Author : wangmengmeng
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")