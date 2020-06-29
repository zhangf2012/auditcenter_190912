# -*- coding: utf-8 -*-
# @Time : 2019/7/24 16:59
# @Author : wangmengmeng
import unittest
import json
import warnings
import time
from common.template import Template
from common.logger import Logger
from common.chat import Chat


class TestIm(unittest.TestCase):
    log = Logger("TestIm")

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.tem = Template()
        self.chat = Chat()

    def test_ipt_01(self):
        # 住院只有已审当前任务有记录按钮，其作为合并任务时没有
        engineid1 = self.tem.get_ipt_engineid("ipt", "医嘱一", 1)
        engineid2 = self.tem.get_ipt_engineid("ipt", "医嘱二", 2)
        self.tem.ipt_audit(self.tem.change_data['{{gp}}'], engineid1, 0)  # 审核打回任务一
        self.chat.doc_ipt_send(engineid1, self.tem.change_data['{{gp}}'])
        self.chat.phar_ipt_send(engineid1, self.tem.change_data['{{gp}}'])
        flag = self.chat.ipt_chat_flag(engineid1, self.tem.change_data['{{gp}}'])
        self.assertEqual(flag['data']['chatFlag'], 1)
        res = self.chat.phar_ipt_query_chat(engineid1, self.tem.change_data['{{gp}}'])
        self.assertEqual(len(res['data']), 2)  # 药师端
        res2 = self.chat.doc_ipt_query(engineid1, self.tem.change_data['{{gp}}'])
        self.assertEqual(len(res['data']), 2)

    def test_opt_01(self):
        """同患者产生两个任务"""
        engineid1 = self.tem.get_opt_engineid("opt", "处方一", 1)
        engineid2 = self.tem.get_opt_engineid("opt", "处方二", 2)
        print(engineid1, engineid2)
        self.tem.opt_audit(engineid1, 1)  # 审核打回任务一
        self.chat.doc_opt_send(engineid1)  # 医生发起聊天
        self.chat.phar_opt_send(engineid1)  # 药师也发消息
        # 待审页面查看点击任务二，查看合并任务一，任务一有记录按钮且内容展示正确
        flag1 = self.chat.opt_chat_flag(engineid1, engineid2, 0)
        self.assertEqual(flag1['data'][0]['chatFlag'], 1)
        res = self.chat.phar_query_chat(engineid1)
        self.assertEqual(len(res['data']), 2)  # 待审记录列表有两条消息
        # 审核任务二
        self.tem.opt_audit(engineid2, 2)
        # 已审页面查看任务一，有记录按钮且内容展示正确；查看任务二，任务一作为合并任务有记录按钮且内容展示正确，三处的记录列表调用的同一个接口，则只在待审验证即可
        # 任务一展示记录按钮
        flag2 = self.chat.opt_chat_flag(engineid1, engineid1, 1)
        self.assertEqual(flag2['data'][0]['chatFlag'], 1)
        flag3 = self.chat.opt_chat_flag(engineid1, engineid2, 1)
        self.assertEqual(flag3['data'][0]['chatFlag'], 1)
        res = self.chat.doc_opt_query(engineid1)
        self.assertEqual(len(res['data']), 2)

