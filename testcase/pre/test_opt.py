# -*- coding: utf-8 -*-
# @Time : 2019/8/22 15:20
# @Author : wangmengmeng
from common.logger import log
from common.opt import Opt
import unittest
import warnings
from common.send_data_new import send

class TestOpt(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.opt = Opt()

    def test_01(self):
        send.send('opt','处方a',1)
