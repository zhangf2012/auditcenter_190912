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
        self.auditcenter_url = self.conf.get('auditcenter', 'address')
        self.request = HttpRequest()

    @wait
    def selNotAuditOptList(self, num):
        """
        待审门诊列表根据处方号查询
        :return:   通过return结果可以获得以下数据：engineid res['data']['optRecipeList'][0]['id']
        """
        url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/selNotAuditOptList'
        recipeno = 'r' + ''.join(str(num)) + '_' + self.send.change_data['{{ts}}']
        param = {
            "recipeNo": recipeno
        }
        res = self.request.post_json(url, param)
        return res

    @wait
    def waitOptList(self, num):
        """
        待审门诊列表根据处方号查询
        :return:   通过return结果可以获得以下数据：engineid res['data']['optRecipeList'][0]['id']
        """
        # self.send.send('ipt', '医嘱一', 1)
        # time.sleep(3)
        url = self.conf.get('auditcenter', 'address') + '/api/v1/opt/selNotAuditOptList'
        recipeno = 'r' + ''.join(str(num)) + '_' + self.send.change_data['{{ts}}']
        param = {
            "recipeNo": recipeno
        }
        res = self.request.post_json(url, param)
        optRecipeList = res['data']['optRecipeList']  # 待审列表的处方数据
        infos = []
        engineid = ''
        if optRecipeList is not None:  # 待审列表的处方不为空的时候执行下述语句
            infos = res['data']['optRecipeList'][0]['infos']
            engineid = res['data']['optRecipeList'][0]['optRecipe']['id']
        return optRecipeList, infos, engineid

    def get_engineid(self, num):
        """
        待审列表获取引擎id
        :param num: 根据处方号获取引擎id，注意看xml中处方号r后拼接的是1还是2
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
        url = ''
        param = ''
        if audit_type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/detailPageAuditRefuse?auditWay=2'
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回必须修改",
                "operationRecordList": [],
                "messageStatus": 0
            }
        elif audit_type == 1:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/detailPageAuditRefuse?auditWay=2'
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回可双签",
                "operationRecordList": [],
                "messageStatus": 1
            }
        elif audit_type == 2:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/detailPageAuditAgree?auditWay=2'
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

    def mergeAuditResult(self, recipeId, id, type):
        """
        获取处方的操作(干预理由、药师、医生等)记录
        :param recipeId:  第一次跑引擎的engineid
        :param id:  第二次跑引擎的engineid
        :param type: type = 0代表待审页面，type = 1代表已审页面
        :return:
        """
        if type == 0:
            url = (self.auditcenter_url + "/api/v1/opt/mergeAuditResult?recipeId=%s&id=%s") % (recipeId, id)
        else:
            url = (self.auditcenter_url + "/api/v1/opt/all/mergeAuditResult?recipeId=%s&id=%s") % (recipeId, id)
        return self.request.get(url)
