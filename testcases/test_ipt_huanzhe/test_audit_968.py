# -*- coding: utf-8 -*-
# @Time : 2020/4/3 15:56
# @Author : wangmengmeng
import pytest


@pytest.mark.ipt_delete
class TestAudit_968:
    """删除相关的测试用例"""

    def test_01(self, zy):
        """
        操作步骤：
        1.开具医嘱包含两组药产生待审任务，且药师未审核
        2.删除其中一组药
        3.删除另外一组药

        期望：
        1时产生待审任务，2时待审任务中只剩一组药，3时待审任务撤销
        """
        zy.send.send('ipt', 'audit986_1', 1)
        zy.send.send('ipt', 'audit986_2', 1)
        engineid = zy.get_engineid(1)
        assert zy.selNotAuditIptList()
        zy.send.send('ipt', 'audit986_3', 1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']

    def test_02(self, zy):
        """
        步骤：
        1.开具包含两组药的医嘱且药师审核（称为任务一）
        2.同患者再次开具包含一组药的医嘱，产生待审任务后药师未审核（称为任务二，其合并任务为任务一）
        3.调用删除接口删除2中的其中一组药
        期望：
        待审任务二撤回
        """
        zy.send.send('ipt', 'audit986_1', 1)
        # zy.send.send('ipt', 'audit986_2', 2)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(engineid1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']
        zy.send.send('ipt', 'audit986_4', 1)
        # zy.send.send('ipt', 'audit986_5', 1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']

    def test_04(self, zy):
        """
        步骤：


        
        1.开具包含两组药的医嘱且药师审核（称为任务一）
        2.同患者再次开具包含两组药的医嘱，产生待审任务后药师未审核（称为任务二，其合并任务为任务一）
        3.调用删除接口删除2中的其中一组药
        期望：
        待审任务二撤回重新产生新任务（当前任务中只剩未删的那组药）
        """
        zy.send.send('ipt', 'audit986_1', 1)
        # zy.send.send('ipt', 'audit986_2', 2)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(engineid1)
        assert not zy.selNotAuditIptList()['data']['taskNumList']
        zy.send.send('ipt', 'audit986_6', 1)
        zy.send.send('ipt', 'audit986_5', 2)
        assert zy.selNotAuditIptList()['data']['taskNumList']
