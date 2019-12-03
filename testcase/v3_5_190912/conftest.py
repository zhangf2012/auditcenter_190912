# -*- coding: utf-8 -*-
# @Time : 2019/10/30 14:54
# @Author : wangmengmeng

import pytest
from common.opt import Opt
from common.ipt import Ipt


@pytest.fixture(scope='function')
def mz():
    opt = Opt()
    yield opt
    print("门诊用例执行结束...")


@pytest.fixture(scope='function')
def zy():
    ipt = Ipt()
    yield ipt
    print("住院用例执行结束...")
