# -*- coding: utf-8 -*-
# @Time : 2020/5/7 10:49
# @Author : wangmengmeng
import time


class TestAudit_970:
    def test_01(self, zy):
        zy.send.send('ipt', 'audit970_1', 1)
        engineid = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid, 1)
        zy.send.send('ipt', 'audit970_2', 3)
        zy.send.send('ipt', 'audit970_3', 1)
        time.sleep(10)
        # assert (zy.selNotAuditIptList())['data']['engineInfos']
