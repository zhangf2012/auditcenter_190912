# -*- coding: utf-8 -*-
# @Time : 2020/4/2 10:01
# @Author : wangmengmeng
import pytest
from common.alter_config import AlterConfig


@pytest.fixture(scope="session")
def opt_recipe():
    """修改配置项-门诊处方审查模式 为按处方"""
    ac = AlterConfig()
    ac.alter_sys_config(40041, 1)