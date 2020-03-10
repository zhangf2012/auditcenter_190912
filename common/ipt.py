# -*- coding: utf-8 -*-
# @Time : 2019/8/6 16:28
# @Author : wangmengmeng
from common.request import HttpRequest
from config.read_config import ReadConfig
from common.send_data import SendData
from common.connect_db import ConnectDB
import time


def wait(func):
    # func(*args, **kw)可以使函数适配任意多的参数
    def wrapper(*args, **kw):
        time.sleep(3)
        return func(*args, **kw)

    return wrapper


class Ipt:
    def __init__(self):
        self.send = SendData()
        self.conf = ReadConfig()
        self.request = HttpRequest()
        self.db = ConnectDB()
        self.conn = self.db.connect(self.db.db_sys)
        self.cur = self.db.get_cur(self.conn)
        username = self.conf.get('login', 'username')
        sql = self.conf.get('sql', 'zoneid')
        self.zoneid = (self.db.execute(self.cur, sql))[0]
        # sql_uid = self.conf.get('sql', 'userid')
        # self.uid = (self.db.execute_pid(self.cur, sql_uid, username))[0]

    @wait
    def selNotAuditIptList(self):
        """
        待审住院列表根据患者号查询
        :return:   通过return结果可以获得以下数据：engineid res['data']['engineInfos'][0]['id']
        """
        # self.send.send('ipt', '医嘱一', 1)
        # time.sleep(3)
        url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/selNotAuditIptList'
        param = {
            "patientId": self.send.change_data['{{ts}}']
        }
        res = self.request.post_json(url, param)
        return res

    @wait
    def waitIptList(self):
        """
        待审住院列表根据患者号查询 作用同函数selNotAuditIptList(),是其优化版本
        :return:   通过return结果可以获得以下等数据：engineid res['data']['engineInfos'][0]['id']
        """
        # self.send.send('ipt', '医嘱一', 1)
        # time.sleep(3)
        url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/selNotAuditIptList'
        param = {
            "patientId": self.send.change_data['{{ts}}']
        }
        res = self.request.post_json(url, param)
        engineInfos = res['data']['engineInfos']  # 待审列表的医嘱数据
        engineMsg = []
        engineids = []
        if engineInfos is not None:  # 待审列表有数据的时候执行下述语句
            engineMsg = res['data']['engineInfos'][0]['engineMsg']  # 医嘱对应的警示信息
            engineids = [i['id'] for i in res['data']['engineInfos']]  # 同一患者的所有引擎id
        return engineInfos, engineMsg, engineids

    def get_engineid(self, n):
        """
        待审列表获取引擎id
        :param n: 如果某患者有多条待审任务则会有多个引擎id，n代表取第几个引擎id
        :return:
        """
        res = self.selNotAuditIptList()
        return res['data']['engineInfos'][n - 1]['id']

    def audit_multi(self, *ids):
        """
        待审住院任务列表批量通过
        :param ids:  引擎id
        """
        url = self.conf.get('auditcenter', 'address') + '/api/v1/auditBatchAgree'
        param = {
            "ids": ids,
            "auditType": 3,  # 3指住院
            "auditWay": 2
        }
        self.request.post_json(url, param)

    def ipt_audit(self, gp, engineid, audit_type):
        """
        医嘱详情审核任务
        :param gp:
        :param engineid:
        :param audit_type: 0 审核打回  1 审核打回（可双签） 2 审核通过
        orderType : 1：药物医嘱； 2：非药物医嘱；3：草药医嘱
        """
        url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/auditSingle'
        param = ''
        if audit_type == 0:
            param = {
                "groupOrderList": [{
                    "auditBoList": [],
                    "groupNo": gp,
                    "auditInfo": "必须修改",
                    "auditStatus": 0,
                    "engineId": engineid,
                    "orderType": 1
                }]
            }
        elif audit_type == 1:
            param = {
                "groupOrderList": [{
                    "auditBoList": [],
                    "groupNo": gp,
                    "auditInfo": "打回可双签",
                    "auditStatus": 0,
                    "engineId": engineid,
                    "orderType": 1,
                    "messageStatus": 1
                }]
            }
        elif audit_type == 2:
            param = {
                "groupOrderList": [{
                    "auditBoList": [],
                    "groupNo": gp,
                    "auditInfo": "审核通过",
                    "auditStatus": 1,
                    "engineId": engineid,
                    "orderType": 1
                }]
            }
        self.request.post_json(url, param)

    def orderList(self, engineid, type):
        """
        获取药嘱信息
        :param engineid:
        :param type: 0 待审页面 1 已审页面
        :return:
        """
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/orderList' + '?id=' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/orderList' + '?id=' + str(engineid)
        return self.request.get(url)

    def herbOrderList(self, engineid, type):
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/herbOrderList' + '?id=' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/herbOrderList' + '?id=' + str(engineid)
        return self.request.get(url)

    # def mergeEngineMsgList(self, engineid, type, gno):
    #     """获取医嘱详情右侧的审核记录、警示信息等信息"""
    #     ol = self.orderList(engineid, type)
    #     hl = self.herbOrderList(engineid, type)
    #     medicalIds = []
    #     medicalHisIds = []
    #     herbMedicalIds = []
    #     herbMedicalHisIds = []
    #     if ol['data']:
    #         medicalIds = [i['id'] for i in ol['data'][gno]]
    #         medicalHisIds = [i['orderId'] for i in ol['data'][gno]]
    #     if hl['data']:
    #         herbMedicalIds = [i['drugId'] for i in hl['data'][0]['itemList']]
    #         herbMedicalHisIds = [i['herbMedicalId'] for i in hl['data'][0]['itemList']]
    #     if type == 0:
    #         url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/mergeEngineMsgList'
    #         param = {
    #             "auditWay": 2,
    #             "engineId": engineid,
    #             "zoneId": self.zoneid,
    #             "groupNo": gno,
    #             "medicalIds": medicalIds,
    #             "medicalHisIds": medicalHisIds,
    #             "herbMedicalIds": herbMedicalIds,
    #             "herbMedicalHisIds": herbMedicalHisIds
    #         }
    #     else:
    #         url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/mergeEngineMsgList'
    #         param = {
    #             "engineId": engineid,
    #             "zoneId": self.zoneid,
    #             "groupNo": gno,
    #             "medicalIds": medicalIds,
    #             "medicalHisIds": medicalHisIds,
    #             "herbMedicalIds": herbMedicalIds,
    #             "herbMedicalHisIds": herbMedicalHisIds
    #         }
    #     return self.request.post_json(url, param)
    def mergeEngineMsgList(self, engineid, type, gno):
        """获取医嘱详情右侧的审核记录、警示信息等信息"""
        ol = self.orderList(engineid, type)
        # hl = self.herbOrderList(engineid, type)
        medicalIds = []
        medicalHisIds = []
        if ol['data']:
            medicalIds = [i['id'] for i in ol['data'][gno]]
            medicalHisIds = [i['orderId'] for i in ol['data'][gno]]
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/mergeEngineMsgList'
            param = {
                "auditWay": 2,
                "engineId": engineid,
                "zoneId": self.zoneid,
                "groupNo": gno,
                "medicalIds": medicalIds,
                "medicalHisIds": medicalHisIds,
                "herbMedicalIds": [],
                "herbMedicalHisIds": []
            }
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/mergeEngineMsgList'
            param = {
                "engineId": engineid,
                "zoneId": self.zoneid,
                "groupNo": gno,
                "medicalIds": medicalIds,
                "medicalHisIds": medicalHisIds,
                "herbMedicalIds": [],
                "herbMedicalHisIds": []
            }
        return self.request.post_json(url, param)

    def get_patient(self, engineid, type):
        """获取住院患者信息"""
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/iptPatient' + '?id=' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/iptPatient' + '?id=' + str(engineid)
        return self.request.get(url)

    def get_operation(self, engineid, type):
        """获取住院手术信息"""
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/operationList' + '?id=' + str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + '/api/v1/ipt/all/operationList' + '?id=' + str(engineid)
        return self.request.get(url)

    def isIptCollected(self, engineid, gno):
        ol = self.orderList(engineid, type)
        medicalIds = [i['id'] for i in ol['data'][gno]]
        medicalHisIds = [i['orderId'] for i in ol['data'][gno]]
        url = self.conf.get('auditcenter', 'address') + '/api/v1/collect/isIptCollected'
        param = {
            "collectPeopleId": self.uid,
            "engineId": engineid,
            "groupNo": gno,
            "herbMedicalIds": [],
            "medicalIds": medicalIds
        }
        return self.request.post_json(url, param)


if __name__ == '__main__':
    ipt = Ipt()
    ipt.send.send('ipt', '医嘱一', 1)
    ipt.send.send('ipt', '医嘱二', 1)
    res = ipt.get_engineid(1)
    print(res)
    res = ipt.get_engineid(2)
    print(res)
