# -*- coding: utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : wangmengmeng
import pytest
from common.alter_config import AlterConfig
from common.ipt import Ipt


@pytest.fixture(scope="session",autouse=True)
def ipt_huanzhe():
    """修改配置项-住院医嘱审查模式 为按患者"""
    ac = AlterConfig()
    ac.alter_sys_config(40003, 0)
    # ac.alter_sys_config(40106, 120)


@pytest.fixture(scope='function')
def zy():
    ipt = Ipt()
    yield ipt
    print("住院用例执行结束...")