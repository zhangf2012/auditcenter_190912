# -*- coding: utf-8 -*-
# @Time : 2019/12/27 10:22
# @Author : wangmengmeng
import pytest

c = 3


@pytest.mark.parametrize("a,b", [(c, 1),])
def test_01(a, b):
    print(a)
    print(b)


