# -*- coding: utf-8 -*-
# @Time : 2019/12/17 11:10
# @Author : wangmengmeng
import pytest
import allure


@allure.feature('验证医嘱明细页面审核医嘱药师审核记录展示正确')
class TestAuditIpt:
    """住院单一审核测试用例"""

    @allure.story('住院待审页面当前任务-无审核记录')
    def test_wait_ipt(self, zy):
        """待审页面当前任务-无审核记录"""
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid = zy.get_engineid(1)
        res = zy.mergeEngineMsgList(engineid, 0, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits']
        expected = None
        assert actual == expected

    @allure.story("验证针对不同的审核方式待审页面合并任务的审核记录展示正确")
    @pytest.mark.parametrize("audit_type,expected", [(None, None), (2, 1)],
                             ids=["未审核", "审核通过"])
    # (0, 0), (1, 0), "审核打回(必须修改)", "审核打回(可双签)"  审核打回不会被合并
    def test_wait_ipt_merge(self, zy, audit_type, expected):
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

    @allure.story("验证针对不同的审核方式已审页面当前任务的审核记录展示正确")
    @pytest.mark.parametrize("audit_type,expected", [(2, 1)])
    # (0, 0), (1, 0) 审核打回的任务不被合并
    def test_already_ipt(self, zy, audit_type, expected):
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid, audit_type)
        res = zy.mergeEngineMsgList(engineid, 1, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits'][0]['auditStatus']
        assert actual == expected

    @allure.story("验证针对不同的审核方式已审页面合并任务的审核记录展示正确")
    @pytest.mark.parametrize("audit_type,expected", [(2, 1)])
    # (0, 0), (1, 0) 审核打回的任务不被合并
    def test_already_ipt_merge(self, zy, audit_type, expected):
        zy.send.send('mainscene', 'ipt_1', 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid1, audit_type)
        zy.send.send('mainscene', 'ipt_2', 1)
        engineid2 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{cgp}}'], engineid2, 2)
        res = zy.mergeEngineMsgList(engineid2, 1, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits'][0]['auditStatus']
        assert actual == expected


@pytest.mark.skip(reason="门诊的测试用例我暂时不需要维护")
@allure.feature('验证处方明细页面审核处方药师审核记录展示正确')
class TestAuditOpt:
    """门诊单一审核测试用例"""

    @allure.story('门诊当前任务')
    def test_wait_opt(self, mz):
        """待审当前任务"""
        mz.send.send('mainscene', 'opt_1', 1)
        engineid = mz.get_engineid(1)
        res = mz.mergeAuditResult(engineid, engineid, 0)
        actual = res['data']
        expected = []
        assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(None, []), (0, 0), (1, 0), (2, 1)])
    def test_opt_wait_merge(self, mz, audit_type, expected):
        """待审合并任务"""
        mz.send.send('mainscene', 'opt_1', 1)
        engineid1 = mz.get_engineid(1)
        actual = None
        if audit_type is not None:
            mz.opt_audit(engineid1, audit_type)
            mz.send.send('mainscene', 'opt_2', 1)
            engineid2 = mz.get_engineid(2)
            res = mz.mergeAuditResult(engineid1, engineid2, 0)
            actual = res['data'][0]['auditStatus']
            assert actual == expected
        else:
            mz.send.send('mainscene', 'opt_2', 1)
            engineid2 = mz.get_engineid(2)
            res = mz.mergeAuditResult(engineid1, engineid2, 0)
            actual = res['data']
            assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(0, 0), (1, 0), (2, 1)])
    def test_already_opt(self, mz, audit_type, expected):
        """已审页面当前任务"""
        mz.send.send('mainscene', 'opt_1', 1)
        engineid = mz.get_engineid(1)
        mz.opt_audit(engineid, audit_type)
        res = mz.mergeAuditResult(engineid, engineid, 1)
        actual = res['data'][0]['auditStatus']
        assert actual == expected

    @pytest.mark.parametrize("audit_type,expected", [(0, 0), (1, 0), (2, 1)])
    def test_already_opt_merge(self, mz, audit_type, expected):
        """已审页面合并任务"""
        mz.send.send('mainscene', 'opt_1', 1)
        engineid1 = mz.get_engineid(1)
        mz.opt_audit(engineid1, audit_type)
        mz.send.send('mainscene', 'opt_2', 1)
        engineid2 = mz.get_engineid(2)
        mz.opt_audit(engineid2, audit_type)
        res = mz.mergeAuditResult(engineid1, engineid2, 1)
        actual = res['data'][0]['auditStatus']
        assert actual == expected
