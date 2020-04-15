# -*- coding: utf-8 -*-
# @Time : 2020/4/3 15:56
# @Author : wangmengmeng
import pytest


@pytest.mark.ipt_delete
class TestAudit_986:
    """删除相关的测试用例"""

    def test_01(self, zy):
        zy.send.send('ipt', 'audit986_1', 1)
        zy.send.send('ipt', 'audit986_2', 1)
        engineid = zy.get_engineid(1)
        assert zy.selNotAuditIptList()
        zy.send.send('ipt', 'audit986_3', 1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']

    def test_02(self, zy):
        zy.send.send('ipt', 'audit986_1', 1)
        # zy.send.send('ipt', 'audit986_2', 2)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(engineid1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']
        zy.send.send('ipt', 'audit986_4', 1)
        zy.send.send('ipt', 'audit986_5', 1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']

    def test_04(self, zy):
        zy.send.send('ipt', 'audit986_1', 1)
        # zy.send.send('ipt', 'audit986_2', 2)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(engineid1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']
        zy.send.send('ipt', 'audit986_6', 1)
        zy.send.send('ipt', 'audit986_5', 2)
        assert zy.selNotAuditIptList()['data']['taskNumList']
