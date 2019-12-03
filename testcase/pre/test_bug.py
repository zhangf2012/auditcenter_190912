# -*- coding: utf-8 -*-
# @Time : 2019/8/8 17:39
# @Author : wangmengmeng
import unittest
import warnings
import time
from common.ipt import Ipt


class TestBug(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.ipt = Ipt()

    def test_01(self):
        """AUDIT-593"""
        self.ipt.send.send('ipt', 'test1', 1)
        self.ipt.send.send('ipt', 'test2', 1)

    def test_02(self):
        """AUDIT-609"""
        self.ipt.send.send('bug', 'audit609_1', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{gp}}'], engineid, 0)
        self.ipt.send.send('bug', 'audit609_2', 1)





if __name__ == '__main__':
    unittest.main()
