# -*- coding: utf-8 -*-
# @Time : 2019/12/12 15:05
# @Author : wangmengmeng
import pytest
from common.alter_config import AlterConfig
from common.request import HttpRequest
from config.read_config import ReadConfig
import time

sc = AlterConfig()
hq = HttpRequest()
rc = ReadConfig()
url = rc.get('auditcenter', 'address')


class TestSysconfig:
    """测试审方系统在用户中心的配置项是否正确"""

    @pytest.mark.parametrize("value,expected", [(0, 0), (1, 1), (2, 2), (3, 3)])
    def test_40009(self, value, expected):
        """新任务提醒（是否有提示音）"""
        sc.alter_sys_config(40009, value)
        res = hq.get(url + '/api/v1/newTaskHint')
        actual = res['data']['taskHint']
        assert actual == str(expected)

    def test_40011(self):
        """是否显示住院任务剩余时间"""
        pass

    @pytest.mark.parametrize("value,expected_ipt,expected_opt",
                             [("None", "true", False), ("0,0", False, False), ("0,1", "false", "true"),
                              ("1,0", "true", "false"), ("1,1", "true", "true")])
    # 传参为None时，默认住院需要校验，门诊不需要校验
    def test_40028(self, value, expected_ipt, expected_opt):
        """医生操作是否需要验证账号"""
        value = value.strip('"')
        sc.alter_sys_config(40028, value)
        res = hq.get(url + '/api/v1/config/clientDocVerify')
        # pytest.assume(res['data']['iptIsVerify'] == expected_ipt)
        # pytest.assume(res['data']['optIsVerify'] == expected_opt)
        assert res['data']['iptIsVerify'] == expected_ipt

    @pytest.mark.parametrize("value,expected", [("测试双签名", "测试双签名"), (None, "null")])
    # 传参为None时，后端返回空，但是前端会给默认值的，这个需要在页面测试
    def test_40030(self, value, expected):
        """双签名按钮名称"""
        sc.alter_sys_config(40030, value)
        res = hq.get(url + '/api/v1/config/doubleSignName')
        print(res)
        time.sleep(2)
        actual = res['data'].encode("utf-8").decode("unicode_escape")
        assert actual.strip('"') == expected

    @pytest.mark.parametrize("value,expected", [("测试撤销医嘱", "测试撤销医嘱"), (None, "null")])
    # 传参为None时，后端返回空，但是前端会给默认值的，这个需要在页面测试
    def test_40031(self, value, expected):
        """撤销医嘱按钮名称"""
        sc.alter_sys_config(40031, value)
        res = hq.get(url + '/api/v1/config/cancelName')
        actual = res['data'].encode("utf-8").decode("unicode_escape")
        assert actual.strip('"') == expected

    @pytest.mark.parametrize("value,expected", [("测试修改处方", "测试修改处方"), (None, "null")])
    # 传参为None时，后端返回空，但是前端会给默认值的
    def test_40032(self, value, expected):
        """修改处方按钮名称"""
        sc.alter_sys_config(40032, value)
        res = hq.get(url + '/api/v1/config/modifyName')
        actual = res['data'].encode("utf-8").decode("unicode_escape")
        assert actual.strip('"') == expected

    def test_40058(self):
        """是否显示门诊任务剩余时间"""
        pass

    def test_40100(self):
        """是否隐藏“打回（可双签）”按钮"""
        """
        api/v1/ipt/all/orderList
        api/v1/ipt/all/herbOrderList
        api/v1/opt/all/recipeInfo
        """
        pass

    def test_40101(self):
        """是否隐藏双签按钮"""
        """
        api/v1/reject/getIptBackTaskDetail
        api/v1/reject/getOptBackTaskDetail rdsiType(String)
        """
        pass
