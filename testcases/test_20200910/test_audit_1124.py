# -*- coding: utf-8 -*-
# @Time : 2020/6/16 14:11
# @Author : wangmengmeng
class TestAudit1124:
    def test_01(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_2', 1)  # 减少一个药
        zy.send.send('ipt', 'audit771_16', 1)

        pass

    def test_02(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_3', 1)  # 只修改药品信息，药品个数不变
        zy.send.send('ipt', 'audit771_16', 1)

        pass

    def test_03(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_4', 1)  # 增加一个药
        zy.send.send('ipt', 'audit771_16', 1)

        pass
