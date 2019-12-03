# -*- coding: utf-8 -*-
# @Time : 2019/8/6 16:28
# @Author : wangmengmeng
from common.request import HttpRequest
from config.read_config import ReadConfig
from common.send_data import SendData
import time


def wait(func):
    # func(*args, **kw)可以使函数适配任意多的参数
    def wrapper(*args, **kw):
        time.sleep(3)
        return func(*args, **kw)

    return wrapper


class Opt:
    def __init__(self):
        self.send = SendData()
        self.conf = ReadConfig()
        self.request = HttpRequest()

    @wait
    def selNotAuditOptList(self, num):
        """
        待审门诊列表根据处方号查询
        :return:   通过return结果可以获得以下数据：engineid res['data']['engineInfos'][0]['id']
        """
        # self.send.send('ipt', '医嘱一', 1)
        # time.sleep(3)
        url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/selNotAuditOptList'
        recipeno = 'r' + ''.join(str(num)) + '_' + self.send.change_data['{{ts}}']
        param = {
            "recipeNo": recipeno
        }
        res = self.request.post_json(url, param)
        return res

    def get_engineid(self, num):
        """
        待审列表获取引擎id
        :param n: 如果某患者有多条待审任务则会有多个引擎id，n代表取第几个引擎id
        :return:
        """
        res = self.selNotAuditOptList(num)
        return res['data']['optRecipeList'][0]['optRecipe']['id']

    def audit_multi(self, *ids):
        """
        待审门诊任务列表批量通过
        :param ids:  引擎id
        """
        url = self.conf.get('auditcenter', 'address') + '/api/v1/auditBatchAgree'
        param = {
            "ids": ids,
            "auditType": 1,  # 1指门急诊
            "auditWay": 2
        }
        self.request.post_json(url, param)

    def opt_audit(self, engineid, audit_type):
        """
        处方详情审核任务
        :param engineid:
        :param audit_type: 0 审核打回  1 审核打回（可双签） 2 审核通过
        """
        url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/auditSingle'
        param = ''
        if audit_type == 0:
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回必须修改",
                "operationRecordList": [],
                "messageStatus": 0
            }
        elif audit_type == 1:
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回可双签",
                "operationRecordList": [],
                "messageStatus": 1
            }
        elif audit_type == 2:
            param = {
                "optRecipeId": engineid,
                "auditResult": "审核通过"
            }
        self.request.post_json(url, param)

    def get_recipeInfo(self, engineid, type):
        """
        获取处方(包括处方头与处方明细)信息与患者信息
        :param engineid:
        :param type: 0 待审页面 1 已审页面
        :return:
        """
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/recipeInfo/' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/all/recipeInfo/' + str(engineid)
        return self.request.get(url)

    def get_operation(self, engineid, type):
        """获取门诊手术信息"""
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/optOperationList/' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/all/optOperationList/' + str(engineid)
        return self.request.get(url)
