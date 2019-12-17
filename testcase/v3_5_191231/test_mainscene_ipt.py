# -*- coding: utf-8 -*-
# @Time : 2019/12/17 11:10
# @Author : wangmengmeng
import pytest


class TestMainsceneIpt:
    def test_wait_ipt(self, zy):
        """待审页面当前任务"""
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid = zy.get_engineid(1)
        res = zy.mergeEngineMsgList(engineid, 0, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits']
        expected = None
        assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(None, None), (0, 0), (1, 0), (2, 1)])
    def test_wait_ipt_merge(self, zy, audit_type, expected):
        """待审页面合并任务"""
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid1 = zy.get_engineid(1)
        actual = None
        if audit_type is not None:
            zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid1, audit_type)
            zy.send.send('mainscene', 'ipt_2', 1)
            engineid2 = zy.get_engineid(1)
            res = zy.mergeEngineMsgList(engineid2, 0, zy.send.change_data['{{gp}}'])
            actual = res['data']['groupAudits'][0]['auditStatus']
        else:
            zy.send.send('mainscene', 'ipt_2', 1)
            engineid2 = zy.get_engineid(2)
            res = zy.mergeEngineMsgList(engineid2, 0, zy.send.change_data['{{gp}}'])
            actual = res['data']['groupAudits']
        assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(0, 0), (1, 0), (2, 1)])
    def test_already_ipt(self, zy, audit_type, expected):
        """已审页面当前任务"""
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid, audit_type)
        res = zy.mergeEngineMsgList(engineid, 1, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits'][0]['auditStatus']
        assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(0, 0), (1, 0), (2, 1)])
    def test_already_ipt_merge(self, zy, audit_type, expected):
        """已审页面合并任务"""
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid1, audit_type)
        zy.send.send('mainscene', 'ipt_2', 1)
        engineid2 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{cgp}}'], engineid2, 2)
        res = zy.mergeEngineMsgList(engineid2, 1, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits'][0]['auditStatus']
        assert actual == expected
