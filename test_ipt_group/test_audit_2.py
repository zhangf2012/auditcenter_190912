# -*- coding: utf-8 -*-
# @Time : 2020/4/2 14:25
# @Author : wangmengmeng
import pytest
from api.audit import Audit
from common.send_data import SendData
from api.ipt_wait import IptWait


class TestAudit:
    """页面审核操作"""
    def test_auditBatchAgree_1(self):
        """单个任务批量通过"""
        s = SendData()
        s.send("mainscene", 'ipt_1', 1)  # 开具医嘱
        engineid = IptWait().selNotAuditIptList(s.change_data["{{ts}}"])['data']['engineInfos'][0]['id']
        Audit().auditBatchAgree(3, engineid)
        assert IptWait().selNotAuditIptList(s.change_data["{{ts}}"]) is not None  # 待审页面不存在该数据
        # 已审列表存在该数据
        # 已审详情药师操作记录为人工审核
        # 药嘱id正确
        # 警示信息正确
    def test_auditBatchAgree_2(self):
        """两个任务批量通过"""
        s = SendData()
        s.send("mainscene", 'ipt_1', 1)  # 开具医嘱
        engineid = IptWait().selNotAuditIptList(s.change_data["{{ts}}"])['data']['engineInfos'][0]['id']
        Audit().auditBatchAgree(3, engineid)
        assert IptWait().selNotAuditIptList(s.change_data["{{ts}}"]) is not None

    """勾选警示信息审核通过"""
    """填写人工意见审核通过"""
    """勾选警示信息并填写人工意见审核通过"""


