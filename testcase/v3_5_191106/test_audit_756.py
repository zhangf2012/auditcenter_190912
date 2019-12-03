# -*- coding: utf-8 -*-
# @Time : 2019/10/31 11:24
# @Author : wangmengmeng
import pytest


class TestIpt:
    """AUDIT-756 患者模式下，已产生的待审任务调用删除接口删除所有组医嘱，该任务应撤销"""

    def test_delete(self, zy):
        """待审页面，删除（调用删除接口）任务内所有组医嘱后，待审任务撤销"""
        zy.send.send('ipt', 'audit756_1', 1)  # 开具医嘱
        zy.send.send('ipt', 'audit756_2', 2)  # 删除医嘱
        zy.send.send('ipt', 'audit756_3', 2)  # 删除医嘱
        assert not (zy.selNotAuditIptList())['data']['engineInfos']


if __name__ == '__main__':
    pytest.main(['-vs', 'test_audit_756.py'])
