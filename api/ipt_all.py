# -*- coding: utf-8 -*-
# @Time : 2020/4/2 14:33
# @Author : wangmengmeng
from common.request import HttpRequest
from config.config import *
from common.connect_db import ConnectDB

r = HttpRequest()


class IptAll:
    def __init__(self):
        db = ConnectDB()
        conn = db.connect(db.db_sf_full)
        self.cur = db.get_cur(conn)

    def iptList(self, startTime=None, endTime=None, antibacterialsFlag=None, injectableFlag=None, eventNo=None,
                patientId=None, auditDocId=None, orderStatus=None, groupNo=None, orderType=None):
        # 注意：auditDocId是int类型，groupNo是str类型,orderStatus是str类型,
        json_data = {
            "antibacterialsFlag": antibacterialsFlag,
            "auditDocId": auditDocId,
            "collectCondition": None,
            "currentPage": "",
            "drugCondition": {
                "drugCodeList": [],
                "drugIdArr": [],
                "drugAdminRouteName": "",
                "drugUsingFreq": "",
                "drugDose": ""
            },
            "endTime": endTime,
            "eventNo": eventNo,
            "groupNo": groupNo,
            "highriskFlag": "",
            "injectableFlag": injectableFlag,
            "orderStatus": orderStatus,
            "orderType": orderType,
            "pageSize": 100,
            "patientId": patientId,
            "startTime": startTime,
            "zoneId": [],
        }
        return r.http_post(auditcennter_url + "/api/v1/ipt/all/iptList", json_data).json()

    def sqlvalue_by_orderStatus(self, orderStatus=None):
        sql = ''
        if orderStatus is None:
            sql = "SELECT COUNT(*) AS '全部医嘱数' FROM sf_ipt_audit_result_item WHERE 1=1"
        elif orderStatus == "0":
            sql = "SELECT COUNT(*) AS '审核打回医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 0"
        elif orderStatus == "1":
            sql = "SELECT COUNT(*) AS '审核通过医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 1"
        elif orderStatus == "2":
            sql = "SELECT COUNT(*) AS '超时通过医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 2;"
        elif orderStatus == "3":
            sql = "SELECT COUNT(*) AS '自动通过医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 3;"
        elif orderStatus == "5":
            sql = "SELECT COUNT(*) AS '人工审核医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 0 OR audit_status = 1;"
        elif orderStatus == "91":
            sql = "SELECT COUNT(*) AS '可双签医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 0 and message_status = 1;"
        elif orderStatus == "90":
            sql = "SELECT COUNT(*) AS '必须修改医嘱数' FROM sf_ipt_audit_result_item WHERE audit_status = 0 and message_status = 0;"
        self.cur.execute(sql)
        count = (self.cur.fetchone())[0]
        return count


if __name__ == '__main__':
    all = IptAll()
    # print(all.iptList(auditDocId=1410))
    print(all.sqlvalue_by_orderStatus("0"))
