# -*- coding: utf-8 -*-
# @Time : 2020/5/21 15:34
# @Author : wangmengmeng
class TestAudit1105:
    def test_01(self,zy):
        zy.send.send('ipt', 'audit1075_1', 1)  # 开医嘱，有失效时间
        zy.send.send('ipt', 'audit771_20', 1)  #删除医嘱
        zy.send.send('ipt', 'audit1075_2', 1)  # 再次开医嘱（同组号同order_id再开医嘱，且其他无字段变更），不产生任务，直接推送审核结果
        pass
