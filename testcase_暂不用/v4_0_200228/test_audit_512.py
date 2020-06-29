# -*- coding: utf-8 -*-
# @Time : 2019/10/31 9:59
# @Author : wangmengmeng
import pytest
import time
from common.alter_config import AlterConfig
from common.connect_db import ConnectDB
from config.read_config import ReadConfig

db = ConnectDB()
conf = ReadConfig()


@pytest.fixture(scope='function')
def implant_config():
    sc = AlterConfig()
    yield sc


class TestIptImplant:
    """AUDIT-512 是否植入物"""

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, None), (0, 1, None), (1, 0, None), (1, 1, None)])
    def test_implant_null(self, zy, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        zy.send.send('ipt', 'audit512_1', 1)
        time.sleep(1)
        engineid = zy.get_engineid(1)
        actual = (zy.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)])
    def test_implant_zero(self, zy, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        zy.send.send('ipt', 'audit512_2', 1)
        time.sleep(1)
        engineid = zy.get_engineid(1)
        actual = (zy.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 1)])
    def test_implant_one(self, zy, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        zy.send.send('ipt', 'audit512_3', 1)
        time.sleep(1)
        engineid = zy.get_engineid(1)
        actual = (zy.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected


class TestOptImplant:
    """AUDIT-512 是否植入物"""

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, None), (0, 1, None), (1, 0, None), (1, 1, None)])
    def test_implant_null(self, mz, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        mz.send.send('opt', 'audit_512_1', 1)
        time.sleep(1)
        engineid = mz.get_engineid(1)
        actual = (mz.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)])
    def test_implant_zero(self, mz, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        mz.send.send('opt', 'audit_512_2', 1)
        time.sleep(1)
        engineid = mz.get_engineid(1)
        actual = (mz.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected

    @pytest.mark.parametrize("is_use,value,expected", [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 1)])
    def test_implant_one(self, mz, implant_config, is_use, value, expected):
        implant_config.alter_default_setting(89, 'whether_Implanta', '是否有植入物', is_use, value)
        mz.send.send('opt', 'audit_512_3', 1)
        time.sleep(1)
        engineid = mz.get_engineid(1)
        actual = (mz.get_operation(engineid, 0))['data'][0]['isImplant']
        assert actual == expected
