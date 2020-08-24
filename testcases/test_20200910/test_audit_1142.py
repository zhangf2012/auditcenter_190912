# -*- coding: utf-8 -*-
# @Time : 2020/8/13 9:51
# @Author : wangmengmeng
import allure


class TestAudit1142:
    def test_01(self, zy):
        """
        步骤：
        1.开医嘱审核打回，且能跑出适应症或禁忌症的警示信息
        2.同患者再次开重复医嘱，且同xml中增加诊断
        断言：2会重新产生待审任务
        :param zy:
        :return:
        """
        zy.send.send('20200910', "audit1142_1", 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid1, 0)  # 药师审核，选择打回
        zy.send.send('20200910', "audit1142_2", 1)  # 增加诊断
        assert (zy.selNotAuditIptList())['data']['engineInfos']  # 会重新产生待审任务

    def test_02(self, zy):
        zy.send.send('20200910', "audit1142_1", 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid1, 0)  # 药师审核，选择打回
        zy.send.send('20200910', "audit1142_3", 1)
        zy.send.send('20200910', "audit1142_4", 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']  # 会重新产生待审任务

    def test_03(self, zy):
        zy.send.send('20200910', "audit1142_1", 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid1, 1)  # 药师审核，选择打回(可双签)
        zy.send.send('20200910', "audit1142_3", 1)  # 传诊断
        zy.send.send('20200910', "audit1142_4", 1)  # 传作废诊断
        assert not (zy.selNotAuditIptList())['data']['engineInfos']  # 不会重新产生待审任务

    def test_04(self, zy):
        zy.send.send('20200910', "audit1142_1", 1)
        engineid1 = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid1, 2)  # 药师审核，选择 通过
        zy.send.send('20200910', "audit1142_3", 1)  # 传诊断
        zy.send.send('20200910', "audit1142_4", 1)  # 传作废诊断
        assert not (zy.selNotAuditIptList())['data']['engineInfos']  # 不会重新产生待审任务
