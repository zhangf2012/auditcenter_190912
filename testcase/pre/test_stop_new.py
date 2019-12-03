# -*- coding: utf-8 -*-
# @Time : 2019/7/29 14:01
# @Author : wangmengmeng

import unittest
import warnings
import time
from common.ipt import Ipt


class TestStop(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.ipt = Ipt()

    def test_01(self):
        '''非新开具医嘱，stop_flag = 0,只修改失效时间且原医嘱未审核，则旧任务撤销重新产生任务--ok'''

        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '1', 1)  # 修改医嘱，失效时间大于等于当前时间
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))

    def test_02(self):
        '''非新开具医嘱，stop_flag = 0,只修改失效时间且原医嘱未审核，则旧任务撤销重新产生任务--ok'''

        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '2', 1)  # 修改医嘱，失效时间小于当前时间
        engineid = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tf1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tf1}}']))
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(2)
        self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_03(self):
        '''非新开具医嘱，stop_flag = 0,只修改失效时间（失效时间大于等于当前时间）且原医嘱已审核，则不产生任务'''
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{gp}}'], engineid, 0)
        self.ipt.send.send('ipt_stop', '1', 1)
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))

    def test_04(self):
        '''非新开具医嘱，stop_flag = 0,只修改失效时间（失效时间小于当前时间）且原医嘱已审核，则不产生任务'''
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{gp}}'], engineid, 0)
        self.ipt.send.send('ipt_stop', '2', 1)
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_05(self):
        '''非新开具医嘱，stop_flag = 1,只修改失效时间且原医嘱未审核，则旧任务撤销'''

        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '4', 1)  # 修改医嘱，失效时间大于等于当前时间
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))

    def test_06(self):
        '''非新开具医嘱，stop_flag = 1,只修改失效时间且原医嘱未审核，则旧任务撤销'''

        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '5', 1)  # 修改医嘱，失效时间小于当前时间
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_07(self):
        '''非新开具医嘱，stop_flag = 1,只修改失效时间（失效时间大于等于当前时间）且原医嘱已审核，则不产生任务'''
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{gp}}'], engineid, 0)
        self.ipt.send.send('ipt_stop', '4', 1)
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))

    def test_08(self):
        '''非新开具医嘱，stop_flag = 1,只修改失效时间（失效时间小于当前时间）且原医嘱已审核，则不产生任务'''
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{gp}}'], engineid, 0)
        self.ipt.send.send('ipt_stop', '5', 1)
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱二', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_09(self):
        """新开具临时医嘱，stop_flag=1"""
        self.ipt.send.send('ipt_stop', '临时医嘱一', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱三', 1)
        engineid2 = self.ipt.get_engineid(1)
        ts = int(time.mktime(time.strptime(self.ipt.send.change_data['{{endtoday}}'], "%Y-%m-%d %H:%M:%S"))) * 1000
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'], ts)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'], ts)

    def test_10(self):
        """新开具临时医嘱，stop_flag=0"""
        self.ipt.send.send('ipt_stop', '临时医嘱二', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱三', 1)
        engineid2 = self.ipt.get_engineid(1)
        ts = int(time.mktime(time.strptime(self.ipt.send.change_data['{{endtoday}}'], "%Y-%m-%d %H:%M:%S"))) * 1000
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'], ts)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'], ts)

    def test_11(self):
        """新开具临时医嘱，stop_flag=1"""
        self.ipt.send.send('ipt_stop', '临时医嘱三', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱三', 1)
        engineid2 = self.ipt.get_engineid(2)
        # self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_12(self):
        """新开具临时医嘱，stop_flag=0"""
        self.ipt.send.send('ipt_stop', '临时医嘱四', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱三', 1)
        engineid2 = self.ipt.get_engineid(2)
        # self.assertEqual((self.ipt.orderList(engineid2, 0))['data'], {})

    def test_13(self):
        '''非新开具草药嘱，stop_flag = 0,只修改失效时间且原医嘱未审核，则旧任务撤销重新产生任务--ok'''

        self.ipt.send.send('ipt_stop', '草药嘱', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '6', 1)  # 修改草药嘱，失效时间大于等于当前时间
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.herbOrderList(engineid, 0))['data'][0]['orderInvalidTime'],int(self.ipt.send.change_data['{{tsb1}}']))
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        engineid2 = self.ipt.get_engineid(2)
        self.assertEqual(
            (self.ipt.herbOrderList(engineid, 0))['data'][0]['orderInvalidTime'],int(self.ipt.send.change_data['{{tsb1}}']))
"""
    def test_14(self):
        '''非新开具草药嘱，stop_flag = 0,只修改失效时间（失效时间大于等于当前时间）且原医嘱已审核，则不产生任务--草药嘱fail，目前产生任务了'''
        self.ipt.send.send('ipt_stop', '草药嘱', 1)
        self.assertIsNotNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        engineid = self.ipt.get_engineid(1)
        self.ipt.ipt_audit(self.ipt.send.change_data['{{cgp}}'], engineid, 0)
        self.ipt.send.send('ipt_stop', '6', 1)
        self.assertIsNone((self.ipt.selNotAuditIptList())['data']['engineInfos'])
        self.ipt.send.send('ipt_stop', '医嘱一', 1)
        engineid2 = self.ipt.get_engineid(1)
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][0]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
        self.assertEqual(
            (self.ipt.orderList(engineid2, 0))['data'][self.ipt.send.change_data['{{gp}}']][1]['orderInvalidTime'],
            int(self.ipt.send.change_data['{{tsb1}}']))
"""