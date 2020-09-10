# -*- coding: utf-8 -*-
# @Time : 2020/8/4 10:01
# @Author : wangmengmeng
import pytest
from config.config import *
from common.request import HttpRequest
from common.ipt import Ipt
import allure


@allure.feature("测试审方方案过滤条件的匹配")
class TestMatchPlan:
    planid = "77002"

    @allure.story('方案匹配成功，产生待审任务')
    @pytest.mark.parametrize("body, xmlname", [({
                                                    "id": 77002,
                                                    "name": "住院修改",
                                                    "category": 2,
                                                    "recipeSource": 0,
                                                    "minStay": None,
                                                    "maxStay": None,
                                                    "drugCategorys": None,
                                                    "drugProperties": None,
                                                    "isOuvas": 0,
                                                    "isPivas": 0,
                                                    "minAge": None,
                                                    "maxAge": None,
                                                    "ageUnit": "岁",
                                                    "costTypes": "",
                                                    "diagnoses": None,
                                                    "icd10": None,
                                                    "userId": "1410",
                                                    "userName": "自动化",
                                                    "createdTime": 1596506727000,
                                                    "modifiedTime": 1596506727000,
                                                    "startTime": "00:00",
                                                    "endTime": "23:59",
                                                    "effectWeek": None,
                                                    "deptList": [],
                                                    "groupList": [],
                                                    "doctorList": [],
                                                    "infoList": None,
                                                    "displayInfoList": None,
                                                    "patientCondition": "",
                                                    "iptWardList": [],
                                                    "weekList": None
                                                }, "audit1124_1")])
    def test_success(self, zy, body, xmlname):
        request = HttpRequest()
        response = request.put(auditcennter_url + "/api/v1/auditPlan/" + TestMatchPlan.planid, body)
        zy.send.send("ipt", xmlname, 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']

    @allure.story('方案匹配失败，不产生待审任务')
    @pytest.mark.parametrize("body, xmlname", [({
                                                    "id": 77002,
                                                    "name": "住院修改",
                                                    "category": 2,
                                                    "recipeSource": 0,
                                                    "minStay": None,
                                                    "maxStay": None,
                                                    "drugCategorys": None,
                                                    "drugProperties": None,
                                                    "isOuvas": 0,
                                                    "isPivas": 0,
                                                    "minAge": None,
                                                    "maxAge": None,
                                                    "ageUnit": "岁",
                                                    "costTypes": "",
                                                    "diagnoses": None,
                                                    "icd10": None,
                                                    "userId": "1410",
                                                    "userName": "自动化",
                                                    "createdTime": 1596506727000,
                                                    "modifiedTime": 1596506727000,
                                                    "startTime": "00:00",
                                                    "endTime": "23:59",
                                                    "effectWeek": None,
                                                    "deptList": [],
                                                    "groupList": [],
                                                    "doctorList": [],
                                                    "infoList": None,
                                                    "displayInfoList": None,
                                                    "patientCondition": "",
                                                    "iptWardList": [],
                                                    "weekList": None
                                                }, "audit1124_1")])

#123
    #456
    # 方案匹配失败不产生待审任务124
    def test_fail(self, zy, body, xmlname):
        request = HttpRequest()
        response = request.put(auditcennter_url + "/api/v1/auditPlan/" + TestMatchPlan.planid, body)
        zy.send.send("ipt", xmlname, 1)
        assert (zy.selNotAuditIptList())['data']['engineInfos']