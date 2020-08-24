# -*- coding: utf-8 -*-
# @Time : 2020/8/17 10:05
# @Author : wangmengmeng
import allure


@allure.link("https://jira.ipharmacare.net/browse/AUDIT-1032")
class TestAudit1032:
    def test01(self, zy):
        """
        患者模式下
        1.开具医嘱组1+组2，并审核通过；
        2.开具医嘱组1（修改1）+组2

        期望:组2不需要再次审核
        """

        zy.send.send('mainscene', 'ipt_new_5', 1)
        engineid1 = zy.get_engineid(1)
        # zy.audit_multi(engineid1)
        zy.send.send('mainscene', 'ipt_new_6', 1)
        engineid2 = zy.get_engineid(1)
        assert zy.orderList(engineid2, 0)['data'][zy.send.change_data["{{cgp}}"]][0]['auditMarkStatus'] is None
        assert zy.orderList(engineid2, 0)['data'][zy.send.change_data["{{gp}}"]][0]['auditMarkStatus'] == 1
