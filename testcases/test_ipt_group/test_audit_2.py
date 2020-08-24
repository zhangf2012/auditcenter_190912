# -*- coding: utf-8 -*-
# @Time : 2020/4/2 14:25
# @Author : wangmengmeng
import pytest
from api.audit import Audit
from common.send_data import SendData
from api.ipt_wait import IptWait
import allure


@allure.feature("住院页面审核操作")
class TestAudit:

    @allure.story("单个任务批量通过")
    def test_auditBatchAgree_1(self):
        s = SendData()
        s.send("mainscene", 'ipt_1', 1)  # 开具医嘱
        engineid = IptWait().selNotAuditIptList(s.change_data["{{ts}}"])['data']['engineInfos'][0]['id']
        Audit().auditBatchAgree(3, engineid)
        assert IptWait().selNotAuditIptList(s.change_data["{{ts}}"]) is not None  # 待审页面不存在该数据

    @allure.story("多个任务批量通过")
    def test_auditBatchAgree_2(self):
        s = SendData()
        s.send("mainscene", 'ipt_1', 1)  # 开具医嘱
        engineid = IptWait().selNotAuditIptList(s.change_data["{{ts}}"])['data']['engineInfos'][0]['id']
        Audit().auditBatchAgree(3, engineid)
        assert IptWait().selNotAuditIptList(s.change_data["{{ts}}"]) is not None
