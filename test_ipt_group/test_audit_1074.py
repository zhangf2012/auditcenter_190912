# -*- coding: utf-8 -*-
# @Time : 2020/5/20 13:37
# @Author : wangmengmeng
class TestAudit1074:
    def test_01(self,zy):
        zy.send.send('ipt','audit771_19',1) #开医嘱，有失效时间
        zy.send.send('ipt','audit771_20',1) #开停嘱
        zy.send.send('ipt','audit1074_1',1) # 再次开医嘱（同组号同order_id再开医嘱）
        pass

