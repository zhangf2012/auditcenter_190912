# -*- coding: utf-8 -*-
# @Time : 2020/5/20 16:18
# @Author : wangmengmeng
class TestAudit1062:
    """药师审核打回医嘱不合并"""

    def test_01(self, zy):
        """打回->修改 (未审核) 加入合并"""
        zy.send.send('ipt', 'audit771_36', 1)
        engineid = zy.get_engineid(1)
        zy.send.send('ipt', 'audit771_37', 1)
        zy.send.send('ipt', 'audit771_38', 1)
        pass

    def test_02(self, zy):
        zy.send.send('ipt', 'audit771_38', 1)
        zy.send.send('ipt', 'audit771_36', 1)
        pass
