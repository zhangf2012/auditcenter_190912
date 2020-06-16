# -*- coding: utf-8 -*-
# @Time : 2019/12/9 15:44
# @Author : wangmengmeng
import pytest


# from pytest_assume.plugin import assume
class TestIptNew:
    """新开医嘱"""

    def test_wait_med_01(self, zy):
        """"""
        zy.send.send('ipt', 'audit771_22', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_med_02(self, zy):
        """失效时间大于当前时间"""
        zy.send.send('mainscene', 'new_1', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_med_03(self, zy):
        """失效时间等于当前时间"""
        zy.send.send('mainscene', 'new_2', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_med_04(self, zy):
        """失效时间小于当前时间"""
        zy.send.send('mainscene', 'new_3', 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_med_05(self, zy):
        """1.开具医嘱1，并审核通过；
           2.开具医嘱2（包含医嘱1）产生任务二"""
        zy.send.send('mainscene', 'ipt_new_4', 1)
        zy.send.send('mainscene', 'ipt_new_5', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_med_06(self, zy):
        """"""
        zy.send.send('mainscene', 'ipt_new_4', 1)
        zy.send.send('mainscene', 'ipt_new_4', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_wait_herbmed(self, zy):
        zy.send.send('ipt', 'audit771_23', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']


class TestIptModify:
    """修改医嘱"""

    @pytest.mark.parametrize("xml1,xml2,xml3", [('audit771_36', 'audit771_37', 'audit771_38')])
    def test_ipt_modify_0(self, zy, xml1, xml2, xml3):
        """修改-药嘱-未审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        engineid1 = zy.get_engineid(1)
        res1 = zy.orderList(engineid1, 0)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res1['data'][zy.send.change_data['{{gp}}']]]
        zy.audit_multi(*[engineid1])
        res2 = zy.orderList(engineid1, 1)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res2['data'][zy.send.change_data['{{gp}}']]]
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.orderList(engineid, 0)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res3['data'][zy.send.change_data['{{gp}}']]]
        zy.audit_multi(*[engineid])
        res = zy.orderList(engineid, 1)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res['data'][zy.send.change_data['{{gp}}']]]

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3", [('audit771_36', 'audit771_37', 'audit771_38')])
    def test_ipt_modify_1(self, zy, xml1, xml2, xml3):
        """退药-药嘱-审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(*[engineid1])
        zy.send.send('ipt', xml2, 1)  # 修改会重新产生任务
        res2 = zy.orderList(engineid1, 1)
        assert '忌辛辣修改一下' not in [i['specialPrompt'] for i in res2['data'][zy.send.change_data['{{gp}}']]]
        engineid4 = zy.get_engineid(1)
        res4 = zy.orderList(engineid4, 0)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res4['data'][zy.send.change_data['{{gp}}']]]
        zy.audit_multi(*[engineid4])
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in
                             (zy.orderList(engineid4, 1))['data'][zy.send.change_data['{{gp}}']]]
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.orderList(engineid, 0)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res3['data'][zy.send.change_data['{{gp}}']]]
        zy.audit_multi(*[engineid])
        res = zy.orderList(engineid, 1)
        assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res['data'][zy.send.change_data['{{gp}}']]]

    # @pytest.mark.parametrize("xml1,xml2,xml3", [('audit771_42', 'audit771_43', 'audit771_38')])
    # def test_ipt_modify_2(self, zy, xml1, xml2, xml3):
    #     """order_status=0,却修改了医嘱（实际这种情况是不允许的，此请情况只存在于需要兼容3.5数据但是接口不知道怎么区分修改，给了新增状态到审方）"""
    #     zy.send.send('ipt', xml1, 1)
    #     engineid1 = zy.get_engineid(1)
    #     zy.audit_multi(*[engineid1])
    #     zy.send.send('ipt', xml2, 1)  # 修改会重新产生任务
    #     res2 = zy.mergeEngineMsgList(engineid1, 1)


class TestIptDelCancel:
    @pytest.mark.parametrize("xml1", [('audit771_20')])
    def test_wait_med(self, zy, xml1):
        """传入删除/撤消医嘱时，原任务未审则撤销"""
        zy.send.send('ipt', 'audit771_19', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', xml1, 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_27', 1)
        engineid = zy.get_engineid(1)
        assert not zy.orderList(engineid, 0)['data']

    @pytest.mark.parametrize("xml1", [('audit771_20')])
    def test_already_med(self, zy, xml1):
        """传入删除/撤消药嘱时，原任务已审"""
        zy.send.send('ipt', 'audit771_19', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', xml1, 1)
        res = zy.mergeEngineMsgList(engineid, 1, zy.send.change_data['{{gp}}'])
        actual = res['data']['groupAudits'][0]['rejectStatus']  # 断言已审页面医生操作记录为撤销
        assert actual == 0

    @pytest.mark.parametrize("xml1", [('audit771_25')])
    def test_wait_herbmed(self, zy, xml1):
        """传入删除/撤消草药嘱时，原任务未审则撤销"""
        zy.send.send('ipt', 'audit771_24', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', xml1, 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_28', 1)
        engineid = zy.get_engineid(1)
        assert not zy.herbOrderList(engineid, 0)['data']

    @pytest.mark.parametrize("xml1", [('audit771_25')])
    def test_already_herbmed(self, zy, xml1):
        """传入删除/撤消草药嘱时，原任务已审"""
        zy.send.send('ipt', 'audit771_24', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', xml1, 1)
        res = zy.mergeEngineMsgList(engineid, 1, zy.send.change_data['{{cgp}}'])
        actual = res['data']['groupAudits'][0]['rejectStatus']  # 断言已审页面医生操作记录为撤销
        assert actual == 0


class TestIptStop:
    """停止医嘱测试用例"""

    def test_ipt_stop_01(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        zy.send.send('ipt', 'audit771_17', 1)  # 停止医嘱，失效时间大于等于当前时间，旧任务不撤销会重新取新的失效时间
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])  # 待审页面断言当前任务，以下的断言暂有问题

        zy.audit_multi(engineid1)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])  # 已审页面断言当前任务
        zy.send.send('ipt', 'audit771_16', 1)
        engineid2 = zy.get_engineid(1)
        assert (zy.orderList(engineid2, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])
        assert (zy.orderList(engineid2, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])  # 待审页面根据组号断言合并任务

    def test_ipt_stop_02(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        zy.send.send('ipt', 'audit771_18', 1)  # 停止医嘱，失效时间小于当前时间
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid2 = zy.get_engineid(1)
        # 该行代码断言为没有合并任务
        assert not zy.orderList(engineid2, 0)['data']  # 断言待审页面
        zy.audit_multi(engineid2)
        assert not zy.orderList(engineid2, 1)['data']  # 断言已审页面

    def test_ipt_stop_03(self, zy):
        """开具停止医嘱时原医嘱已审核"""
        zy.send.send('ipt', 'audit771_15', 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']
        engineid = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data['{{gp}}'], engineid, 0)
        zy.send.send('ipt', 'audit771_17', 1)  # 停止医嘱，失效时间大于等于当前时间
        zy.send.send('ipt', 'audit771_16', 1)
        engineid2 = zy.get_engineid(2)
        # 以下两行代码断言为合并任务取最新的失效时间
        assert (zy.orderList(engineid2, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])
        assert (zy.orderList(engineid2, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tsb1}}'])

    def test_ipt_stop_04(self, zy):
        """开具停止医嘱时原医嘱已审核"""
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_18', 1)  # 停止医嘱，失效时间小于当前时间
        zy.send.send('ipt', 'audit771_16', 1)
        engineid2 = zy.get_engineid(1)
        # 该行代码断言为没有合并任务
        assert not zy.orderList(engineid2, 0)['data']


class TestIptStop_new:
    def test_ipt_stop_01(self, zy):
        zy.send.send('ipt', 'audit771_44', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，产生任务
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_ipt_stop_02(self, zy):
        zy.send.send('ipt', 'audit771_45', 1)  # 停止医嘱，失效时间小于(当前时间+120),这里的测试数据失效时间为当前时间+60分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']

    def test_ipt_stop_03(self, zy):
        zy.send.send('ipt', 'audit771_46', 1)  # 停止医嘱，失效时间小于当前时间,这里的测试数据失效时间为当前时间-60分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']

    # 临时医嘱没有走配置项，都会产生任务
    def test_ipt_stop_011(self, zy):
        zy.send.send('ipt', 'audit771_441', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，产生任务
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    def test_ipt_stop_021(self, zy):
        zy.send.send('ipt', 'audit771_451', 1)  # 停止医嘱，失效时间小于(当前时间+120),这里的测试数据失效时间为当前时间+60分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']

    def test_ipt_stop_031(self, zy):
        zy.send.send('ipt', 'audit771_461', 1)  # 停止医嘱，失效时间小于当前时间,这里的测试数据失效时间为当前时间-60分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']

    def test_ipt_stop_04(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        zy.send.send('ipt', 'audit771_44', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，旧任务不撤销会重新取新的失效时间
        engineid = zy.get_engineid(1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']
        assert (zy.orderList(engineid, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid)
        assert (zy.orderList(engineid, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])

    def test_ipt_stop_05(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        zy.send.send('ipt', 'audit771_45', 1)  # 停止医嘱，失效时间小于(当前时间+120),这里的测试数据失效时间为当前时间+60分钟，旧任务撤销
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert not zy.orderList(engineid1, 0)['data']

    def test_ipt_stop_06(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        zy.send.send('ipt', 'audit771_46', 1)  # 停止医嘱，失效时间小于当前时间,这里的测试数据失效时间为当前时间-60分钟，旧任务撤销
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert not zy.orderList(engineid1, 0)['data']

    def test_ipt_stop_07(self, zy):
        """长期医嘱已审，再开停嘱不产生任务"""
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_44', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid1)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])

    def test_ipt_stop_071(self, zy):
        """临时医嘱已审，再开停嘱不产生任务"""
        zy.send.send('ipt', 'audit771_151', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_441', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，不产生任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid1)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])

    def test_ipt_stop_072(self, zy):
        """长期医嘱已审，再开停嘱不产生任务"""
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_44', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，不产生任务
        zy.send.send('ipt', 'audit771_44', 1)
        zy.send.send('ipt', 'audit771_44', 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid1)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])

    def test_ipt_stop_073(self, zy):
        """长期医嘱已审，再开停嘱不产生任务"""
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_44', 1)  # 停止医嘱，失效时间大于等于(当前时间+120),这里的测试数据失效时间为当前时间+180分钟，不产生任务
        zy.send.send('ipt', 'audit771_44', 1)
        zy.send.send('ipt', 'audit771_15', 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        zy.audit_multi(engineid1)
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])
        assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
            zy.send.change_data['{{tb180}}'])

    def test_ipt_stop_08(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_45', 1)  # 停止医嘱，失效时间小于(当前时间+120),这里的测试数据失效时间为当前时间+60分钟，不产生待审任务
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit771_16', 1)
        engineid1 = zy.get_engineid(1)
        assert not zy.orderList(engineid1, 0)['data']

        # engineid1 = zy.get_engineid(1)
        # assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
        #     zy.send.change_data['{{tb60}}'])
        # assert (zy.orderList(engineid1, 0))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
        #     zy.send.change_data['{{tb60}}'])
        # zy.audit_multi(engineid1)
        # assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][0]['orderInvalidTime'] == int(
        #     zy.send.change_data['{{tb60}}'])
        # assert (zy.orderList(engineid1, 1))['data'][zy.send.change_data['{{gp}}']][1]['orderInvalidTime'] == int(
        #     zy.send.change_data['{{tb60}}'])

    def test_ipt_stop_09(self, zy):
        zy.send.send('ipt', 'audit771_15', 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        zy.send.send('ipt', 'audit771_46', 1)  # 停止医嘱，失效时间小于当前时间,这里的测试数据失效时间为当前时间-60分钟，修改医嘱不产生待审任务
        zy.send.send('ipt', 'audit771_48', 1)
        pass
        # assert not (zy.selNotAuditIptList())['data']['engineInfos']
        # zy.send.send('ipt', 'audit771_16', 1)

        # engineid1 = zy.get_engineid(1)
        # assert not zy.orderList(engineid1, 0)['data']


class TestIptReturnDrug:

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7)])
    # @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7),
    #                                                      ('audit771_4', 'audit771_5', 'audit771_6', 7),
    #                                                      ('audit771_7', 'audit771_8', 'audit771_9', None)])
    def test_ipt_return_drug_0(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱-未审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        engineid1 = zy.get_engineid(1)
        res1 = zy.orderList(engineid1, 0)
        actual1 = None
        for i in res1['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual1 = i['despensingNum']
                break
        assert actual1 == 7
        zy.audit_multi(*[engineid1])
        res2 = zy.orderList(engineid1, 1)
        actual2 = None
        for i in res2['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual2 = i['despensingNum']
                break
        assert actual2 == 7
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.orderList(engineid, 0)
        # actual = [i['despensingNum'] for i in res['data'][zy.send.change_data['{{gp}}']] if i['drugName'] == '盐酸多巴胺注射液'][0]
        # actual = [i['despensingNum'] if i['drugName'] == '盐酸多巴胺注射液' else 0 for i in res['data'][zy.send.change_data['{{gp}}']]][0] 这种方法由于actual里存了多个值不好确定我要取哪个
        actual3 = None
        for i in res3['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        zy.audit_multi(*[engineid])
        res = zy.orderList(engineid, 1)
        actual4 = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7)])
    def test_ipt_return_drug_1(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱-审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(*[engineid1])
        zy.send.send('ipt', xml2, 1)
        res2 = zy.orderList(engineid1, 1)
        actual2 = None
        for i in res2['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual2 = i['despensingNum']
                break
        assert actual2 == 9
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.orderList(engineid, 0)
        actual3 = None
        for i in res3['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        zy.audit_multi(*[engineid])
        res = zy.orderList(engineid, 1)
        actual4 = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7

    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_10', 'audit771_11', 'audit771_12', 7)])
    # @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_10', 'audit771_11', 'audit771_12', 1),
    #                                                      ('audit771_10', 'audit771_13', 'audit771_12', None)])
    def test_ipt_return_drug_3(self, zy, xml1, xml2, xml3, expected):
        """退药-草药嘱-未审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        engineid1 = zy.get_engineid(1)
        res1 = zy.herbOrderList(engineid1, 0)
        actual1 = None
        for i in res1['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual1 = i['despensingNum']
                break
        assert actual1 == 7
        zy.audit_multi(*[engineid1])
        res2 = zy.herbOrderList(engineid1, 1)
        actual2 = None
        for i in res2['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual2 = i['despensingNum']
                break
        assert actual2 == 7
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.herbOrderList(engineid, 0)
        # actual = [i['despensingNum'] for i in res['data'][zy.send.change_data['{{gp}}']] if i['drugName'] == '盐酸多巴胺注射液'][0]
        # actual = [i['despensingNum'] if i['drugName'] == '盐酸多巴胺注射液' else 0 for i in res['data'][zy.send.change_data['{{gp}}']]][0] 这种方法由于actual里存了多个值不好确定我要取哪个
        actual3 = None
        for i in res3['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        zy.audit_multi(*[engineid])
        res = zy.herbOrderList(engineid, 1)
        actual4 = None
        for i in res['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7

    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_10', 'audit771_11', 'audit771_12', 7)])
    def test_ipt_return_drug_4(self, zy, xml1, xml2, xml3, expected):
        zy.send.send('ipt', xml1, 1)
        engineid1 = zy.get_engineid(1)
        zy.audit_multi(*[engineid1])
        zy.send.send('ipt', xml2, 1)
        res2 = zy.herbOrderList(engineid1, 1)
        actual2 = None
        for i in res2['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual2 = i['despensingNum']
                break
        assert actual2 == 9
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(1)
        res3 = zy.herbOrderList(engineid, 0)
        actual3 = None
        for i in res3['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        zy.audit_multi(*[engineid])
        res = zy.herbOrderList(engineid, 1)
        actual4 = None
        for i in res['data'][0]['itemList']:
            if i['drugName'] == 'EW正天丸':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7


@pytest.mark.skip(reason="门诊的测试用例我暂时不需要维护")
class TestOptNew:
    """新开处方"""

    def test_wait(self, mz):
        mz.send.send('opt', 'audit771_35', 1)
        assert (mz.selNotAuditOptList(1))['data']['optRecipeList']


# class TestOptModify:
#     @pytest.mark.parametrize("xml1,xml2,xml3", [('audit771_36', 'audit771_37', 'audit771_38')])
#     def test_opt_modify_0(self, mz, xml1, xml2, xml3):
#         """修改-药嘱-未审核 测试用例"""
#         zy.send.send('ipt', xml1, 1)
#         zy.send.send('ipt', xml2, 1)
#         engineid1 = zy.get_engineid(1)
#         res1 = zy.orderList(engineid1, 0)
#         assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res1['data'][zy.send.change_data['{{gp}}']]]
#         zy.audit_multi(*[engineid1])
#         res2 = zy.orderList(engineid1, 1)
#         assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res2['data'][zy.send.change_data['{{gp}}']]]
#         zy.send.send('ipt', xml3, 1)
#         engineid = zy.get_engineid(1)
#         res3 = zy.orderList(engineid, 0)
#         assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res3['data'][zy.send.change_data['{{gp}}']]]
#         zy.audit_multi(*[engineid])
#         res = zy.orderList(engineid, 1)
#         assert '忌辛辣修改一下' in [i['specialPrompt'] for i in res['data'][zy.send.change_data['{{gp}}']]]

@pytest.mark.skip(reason="门诊的测试用例我暂时不需要维护")
class TestOptDel:
    def test_wait(self, mz):
        mz.send.send('opt', 'audit771_29', 1)
        assert (mz.selNotAuditOptList(1))['data']['optRecipeList']
        mz.send.send('opt', 'audit771_30', 1)
        assert not (mz.selNotAuditOptList(1))['data']['optRecipeList']
        mz.send.send('opt', 'audit771_31', 1)
        engineid = mz.get_engineid(2)
        # assert 'r1' in  mz.get_recipeInfo(engineid, 0)['data']['optRecipe'][1]  # 有合并处方
        check = 'r1' not in mz.get_recipeInfo(engineid, 0)['data']['optRecipe']
        assert 'r1' not in mz.get_recipeInfo(engineid, 0)['data']['optRecipe']  # 无合并出处方
        # assert check


@pytest.mark.skip(reason="门诊的测试用例我暂时不需要维护")
class TestOptReturnDrug:
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_32', 'audit771_33', 'audit771_34', 7)])
    def test_opt_return_drug_0(self, mz, xml1, xml2, xml3, expected):
        """退药-原处方未审核 测试用例"""
        mz.send.send('opt', xml1, 1)
        mz.send.send('opt', xml2, 1)
        engineid1 = mz.get_engineid(1)
        res1 = mz.get_recipeInfo(engineid1, 0)
        actual1 = None
        for i in res1['data']['optRecipe'][0]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual1 = i['despensingNum']
                break
        assert actual1 == 7
        mz.audit_multi(*[engineid1])
        res2 = mz.get_recipeInfo(engineid1, 1)
        actual2 = None
        for i in res2['data']['optRecipe'][0]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual2 = i['despensingNum']
                break
        assert actual2 == 7
        mz.send.send('opt', xml3, 1)
        engineid = mz.get_engineid(2)
        res3 = mz.get_recipeInfo(engineid, 0)
        actual3 = None
        for i in res3['data']['optRecipe'][1]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        mz.audit_multi(*[engineid])
        res = mz.get_recipeInfo(engineid, 1)
        actual4 = None
        for i in res['data']['optRecipe'][1]['mapItems'][mz.send.change_data['{{gp}}']]:  # 合并任务索引是1
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_32', 'audit771_33', 'audit771_34', 7)])
    def test_opt_return_drug_1(self, mz, xml1, xml2, xml3, expected):
        """退药-审核 测试用例"""
        mz.send.send('opt', xml1, 1)
        engineid1 = mz.get_engineid(1)
        mz.audit_multi(*[engineid1])
        mz.send.send('opt', xml2, 1)
        res2 = mz.get_recipeInfo(engineid1, 1)
        actual2 = None
        for i in res2['data']['optRecipe'][0]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual2 = i['despensingNum']
                break
        assert actual2 == 9
        mz.send.send('opt', xml3, 1)
        engineid = mz.get_engineid(2)
        res3 = mz.get_recipeInfo(engineid, 0)
        actual3 = None
        for i in res3['data']['optRecipe'][1]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual3 = i['despensingNum']
                break
        assert actual3 == 7
        mz.audit_multi(*[engineid])
        res = mz.get_recipeInfo(engineid, 1)
        actual4 = None
        for i in res['data']['optRecipe'][1]['mapItems'][mz.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸维拉帕米注射液':
                actual4 = i['despensingNum']
                break
        assert actual4 == 7


if __name__ == '__main__':
    pytest.main()
