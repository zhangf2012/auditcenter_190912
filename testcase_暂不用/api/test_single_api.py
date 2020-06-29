# -*- coding: utf-8 -*-
# @Time : 2019/12/4 22:08
# @Author : wangmengmeng
import pytest
from common.request import HttpRequest
from common.handle_yaml import HandleYaml

requ = HttpRequest()
hy = HandleYaml()
datas = hy.read_yaml('auditcenter.yaml')
print(datas)
auditcenter_url = 'http://10.1.1.89:9999/auditcenter'


@pytest.mark.parametrize("api,method,data,params,headers,assert_code", datas)
def test_single_api(api, method, data, params, headers, assert_code):
    res = requ.req(auditcenter_url + api, method, data, params, headers)
    assert res.json()['code'] == str(assert_code)
