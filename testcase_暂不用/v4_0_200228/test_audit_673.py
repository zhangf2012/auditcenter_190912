# -*- coding: utf-8 -*-
# @Time : 2019/12/17 16:44
# @Author : wangmengmeng
import pytest


class TestGanyuIpt:
    """住院干预双签理由展示测试用例"""

    def test_wait_ipt_01(self, zy):
        """待审页面当前任务"""
        zy.send.send('ipt', 'audit673_1', 1)
        zy.send.send('ipt', 'audit673_2', 1)
        engineid = zy.get_engineid(1)
        res = zy.mergeEngineMsgList(engineid, 0, zy.send.change_data['{{gp}}'])
        actual = len(res['data']['groupAudits'])
        expected = 1
        assert actual == expected

    def test_wait_ipt_02(self, zy):
        """待审页面当前任务"""
        zy.send.send('ipt', 'audit673_5', 1)
        engineid = zy.get_engineid(1)
        res = zy.mergeEngineMsgList(engineid, 0, zy.send.change_data['{{gp}}'])
        actual = len(res['data']['groupAudits'])
        expected = 1
        assert actual == expected

    def test_ipt_merge_01(self, zy):
        """待审页面合并任务"""
        zy.send.send('ipt', 'audit673_1', 1)
        zy.send.send('ipt', 'audit673_2', 1)
        zy.send.send('ipt', 'audit673_3', 1)
        engineid2 = zy.get_engineid(2)
        res = zy.mergeEngineMsgList(engineid2, 0, zy.send.change_data['{{gp}}'])
        actual = len(res['data']['groupAudits'])
        expected = 1
        assert actual == expected

    def test_ipt_merge_02(self, zy):
        """待审页面合并任务"""
        zy.send.send('ipt', 'audit673_2', 1)
        zy.send.send('ipt', 'audit673_4', 1)
        zy.send.send('ipt', 'audit673_3', 1)
        engineid2 = zy.get_engineid(2)
        res = zy.mergeEngineMsgList(engineid2, 0, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits']
        expected = None
        assert actual == expected

    def test_ipt_modify(self, zy):
        zy.send.send('ipt', 'audit673_1', 1)
        zy.send.send('ipt', 'audit673_2', 1)
        zy.send.send('ipt', 'audit673_6', 1)
        engineid1 = zy.get_engineid(1)
        res = zy.mergeEngineMsgList(engineid1, 0, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits']
        expected = None
        assert actual == expected


class TestGanyuOpt:
    """门诊双签理由展示测试用例"""

    def test_wait_opt_01(self, mz):
        """待审页面当前任务"""
        mz.send.send('opt', 'audit673_7', 1)
        mz.send.send('opt', 'audit673_8', 1)
        engineid1 = mz.get_engineid(1)
        res = mz.mergeAuditResult(engineid1, engineid1, 0)
        actual = len(res['data'])
        expected = 1
        assert actual == expected

    def test_wait_opt_02(self, mz):
        """待审页面当前任务"""
        mz.send.send('opt', 'audit673_9', 1)
        engineid1 = mz.get_engineid(1)
        res = mz.mergeAuditResult(engineid1, engineid1, 0)
        actual = len(res['data'])
        expected = 1
        assert actual == expected

    def test_opt_merge_01(self, mz):
        """待审页面合并任务"""
        mz.send.send('opt', 'audit673_10', 1)
        mz.send.send('opt', 'audit673_11', 1)
        mz.send.send('opt', 'audit673_12', 1)
        engineid1 = mz.get_engineid(1)
        engineid2 = mz.get_engineid(2)
        res = mz.mergeAuditResult(engineid1, engineid2, 0)
        actual = len(res['data'])
        expected = 1
        assert actual == expected

    def test_opt_merge_02(self, mz):
        """待审页面合并任务"""
        mz.send.send('opt', 'audit673_11', 1)
        mz.send.send('opt', 'audit673_13', 1)
        mz.send.send('opt', 'audit673_12', 1)
        engineid1 = mz.get_engineid(1)
        engineid2 = mz.get_engineid(2)
        res = mz.mergeAuditResult(engineid1, engineid2, 0)
        actual = res['data']
        expected = []
        assert actual == expected

    def test_opt_modify(self, mz):
        mz.send.send('opt', 'audit673_10', 1)
        mz.send.send('opt', 'audit673_11', 1)
        mz.send.send('opt', 'audit673_14', 1)
        engineid1 = mz.get_engineid(1)
        res = mz.mergeAuditResult(engineid1, engineid1, 0)
        actual = res['data']
        expected = []
        assert actual == expected



