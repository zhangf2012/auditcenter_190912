# -*- coding: utf-8 -*-
# @Time : 2019/12/11 17:13
# @Author : wangmengmeng
import pytest


def test_b():
    globals()["a"] = 1
    assert True


def test_a():
    print("执行测试2")
    print(globals()["a"])
