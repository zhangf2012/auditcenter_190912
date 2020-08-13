# -*- coding: utf-8 -*-
# @Time : 2020/8/4 11:38
# @Author : wangmengmeng
import re
import json


class TestAudit1195:
    def test_med(self, zy):
        # 药嘱
        zy.send.send("20200910", "audit1195_1", 1)
        engineid = zy.get_engineid(1)
        res = zy.orderList(engineid, 0)
        print(type(res))
        # s = """{"code": "200", "message": "OK", "data": {"3068": [{"id": 200273, "zoneId": 11, "eventNo": "1596525890000", "patientId": "1596525890000", "keyDate": 1596525803785, "orderId": "o1_1596525890000", "orderTime": 1596525890000, "orderDeptId": "011", "orderDeptName": "中心ICU", "orderDocId": "wangdoc", "orderDocName": "王医生", "orderDocTitle": "主任医师", "orderType": "临时医嘱", "orderName": null, "orderCategory": null, "orderFreq": null, "orderValidTime": 1596525890000, "orderInvalidTime": 1596556799000, "checkTime": 1596525890000, "checkNurseId": "017", "checkNurseName": "陆羽7", "deptUseOnly": null, "groupNo": "3068", "drugId": "00295600", "drugName": "盐酸多巴胺注射液", "countUnit": 1.0, "packUnit": "片", "manufacturerId": "12", "manufacturerName": "西安杨森制药有限公司", "drugDose": "0.25g", "drugAdminRouteName": "消化道全身给药", "drugUsingFreq": "bid", "drugUsingOpporunity": "餐前", "drugUsingAim": "预防", "drugUsingArea": "肠胃", "drugSource": "1", "duration": "", "preparation": "注射液", "specifications": "5mg", "price": 1.0, "despensingNum": 9.0, "feeTotal": 12.0, "specialPrompt": "忌辛辣", "skinTestTime": 1596439490000, "skinTestFlag": 0, "skinTestResult": "阴性", "updateTime": 1596525803785, "firstUse": null, "exeDeptId": "zx1", "exeDeptName": "执行科室一222222222", "isCancel": null, "orderAuditStatu": null, "isRelated": 0, "isException": null, "specialReturnFlag": 0, "auditMarkStatus": null, "rdsType": "0", "severity": 5, "isCurrentOrder": 1, "docGroup": "神经内科-医生王组", "infusionSpeed": "20滴/分钟", "limitTime": "限用时间", "therapeuticRegimen": "用药方案", "medicareType": "市医保test", "highriskFlag": 0}, {"id": 200274, "zoneId": 11, "eventNo": "1596525890000", "patientId": "1596525890000", "keyDate": 1596525803785, "orderId": "o2_1596525890000", "orderTime": 1596525890000, "orderDeptId": "011", "orderDeptName": "中心ICU", "orderDocId": "wangdoc", "orderDocName": "王医生", "orderDocTitle": "主任医师", "orderType": "临时医嘱", "orderName": null, "orderCategory": null, "orderFreq": null, "orderValidTime": 1596525890000, "orderInvalidTime": 1596556799000, "checkTime": 1596525890000, "checkNurseId": "01", "checkNurseName": "陆羽", "deptUseOnly": null, "groupNo": "3068", "drugId": "00334101", "drugName": "环孢素软胶囊(新山地明)", "countUnit": 6.0, "packUnit": "片", "manufacturerId": "12", "manufacturerName": "西安杨森制药有限公司", "drugDose": "0.2346g", "drugAdminRouteName": "消化道全身给药", "drugUsingFreq": "bid", "drugUsingOpporunity": "餐前", "drugUsingAim": "预防", "drugUsingArea": "肠胃", "drugSource": "1", "duration": "", "preparation": "粉针剂", "specifications": "5mg", "price": 1.0, "despensingNum": 10.0, "feeTotal": 12.0, "specialPrompt": "忌辛辣", "skinTestTime": 1596439490000, "skinTestFlag": 0, "skinTestResult": "阴性", "updateTime": 1596525803785, "firstUse": null, "exeDeptId": "zx1", "exeDeptName": "执行科室一", "isCancel": null, "orderAuditStatu": null, "isRelated": 0, "isException": null, "specialReturnFlag": 0, "auditMarkStatus": null, "rdsType": "0", "severity": 5, "isCurrentOrder": 1, "docGroup": "神经内科-医生王组", "infusionSpeed": "20滴/分钟", "limitTime": "限用时间", "therapeuticRegimen": "用药方案", "medicareType": "市医保test", "highriskFlag": 0}]}}"""
        actual = re.findall(r'"specifications":\s"(\d+\w+)"', json.dumps(res).encode('utf-8').decode('unicode_escape'))[0]
        assert actual == "5mg"

    def test_herbmed(self, zy):
        # 草药嘱
        zy.send.send("20200910", "audit1195_2", 1)
        engineid = zy.get_engineid(1)
        res = zy.herbOrderList(engineid, 0)
        print(type(res))
        actual = re.findall(r'"specifications":\s"(\d+\w+)"', json.dumps(res).encode('utf-8').decode('unicode_escape'))[0]
        assert actual == "3g"
