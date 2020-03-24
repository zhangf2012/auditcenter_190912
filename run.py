# -*- coding: utf-8 -*-
# @Time : 2020/3/24 9:32
# @Author : wangmengmeng
import pytest


if __name__ == '__main__':
    pytest.main(['-vs','--clean-alluredir','--alluredir=allure-results','testcase/v4_0_200228/test_audit_512.py'])