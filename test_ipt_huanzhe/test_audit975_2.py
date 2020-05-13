# -*- coding: utf-8 -*-
# @Time : 2020/5/7 15:59
# @Author : wangmengmeng
class TestAudit_975:
    def test_01(self,zy):
        zy.send.send('ipt', 'audit771_19', 1)
        # assert (zy.selNotAuditIptList())['data']['engineInfos']
        engineid = zy.get_engineid(1)
        zy.ipt_audit(zy.send.change_data["{{gp}}"], engineid, 1)
        zy.send.send('ipt', 'audit771_20', 1)
        # assert not (zy.selNotAuditIptList())['data']['engineInfos']
        zy.send.send('ipt', 'audit975_1', 1)
        assert not (zy.selNotAuditIptList())['data']['engineInfos']
