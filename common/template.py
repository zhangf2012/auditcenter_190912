# -*- coding: utf-8 -*-
# @Time : 2019/6/8 21:40
# @Author : wangmengmeng
import datetime
import hashlib
import json
import os
import random
import re
import time
import requests
from config.read_config import ReadConfig


class Template:
    def __init__(self):
        self.conf = ReadConfig()
        url = self.conf.get('login', 'address') + '/syscenter/api/v1/currentUser'
        username = self.conf.get('login', 'username')
        passwd = self.conf.get('login', 'password')
        m = hashlib.md5()  # 创建md5对象
        m.update(passwd.encode())  # 生成加密字符串
        password = m.hexdigest()
        params = {"name": username, "password": password}
        headers = {'Content-Type': "application/json"}
        self.session = requests.session()
        # self.session.post(url, data=json.dumps(params), headers=headers)
        res = self.session.post(url, data=json.dumps(params), headers=headers).json()  # 登录用户中心
        start_sf_url = self.conf.get('login', 'address') + '/auditcenter/api/v1/startAuditWork'  # 获取开始审方url
        self.session.get(url=start_sf_url)  # 开始审方
        group_no = random.randint(1, 1000000)
        cgroup_no = random.randint(1, 1000000)
        ggroup_no = random.randint(1, 1000000)
        self.change_data = {"{{ts}}": str(self.get_ts(0, 0)),  # 今天时间戳
                            "{{tf2}}": str(self.get_ts(-1, -2)),
                            "{{tf1}}": str(self.get_ts(-1, -1)),
                            "{{t}}": str(self.get_ts(-1, 0)),  # 昨天时间戳
                            "{{d}}": str(self.get_date(-1, 0)),  # 昨天时间
                            "{{tf3}}": str(self.get_ts(-1, -3)),
                            "{{df4}}": str(self.get_date(-1, -4)),
                            "{{tb1}}": str(self.get_ts(-1, +1)),
                            "{{db1}}": str(self.get_date(-1, +1)),
                            "{{dtb1}}": str(self.get_date(+1, 0)), # 明天时间
                            "{{gp}}": str(group_no),
                            "{{cgp}}": str(cgroup_no),
                            "{{ggp}}": str(ggroup_no),
                            "{{df6}}": str(self.get_date(-1, -6)),
                            "{{df3}}": str(self.get_date(-1, -3)),
                            "{{df2}}": str(self.get_date(-1, -1)),
                            "{{df1}}": str(self.get_date(-1, -1)),
                            "{{dt}}": str(self.get_date(0, 0)),  # 今天时间
                            "{{f5}}": str(self.get_date(-5, 0)),
                            "{{f4}}": str(self.get_date(-4, 0)),
                            "{{f3}}": str(self.get_date(-3, 0)),
                            "{{f2}}": str(self.get_date(-2, 0)),
                            }

    # 获取日期格式为%Y-%m-%d %H:%M:%S：，n可取0（表示当前日期），正（表示当前日期+n天），负（表示当前日期-n天）
    def get_ymd(self, d, h):
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d")
        return date

    def get_date(self, d, h):
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d %H:%M:%S")
        return date

    # 获取指定日期的时间戳
    def get_ts(self, d, h):
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d %H:%M:%S")
        ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))  # 获取10位时间戳
        # ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S"))) * 1000   # 获取13位时间戳
        return ts

    def post_json(self, url, para):
        data = para
        data = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        return self.session.post(url, data=data.encode("utf-8"), headers=headers).json()

    def get(self, url):
        return self.session.get(url).json()

    def send_data(self, dir_name, xml_name, **change):
        time.sleep(2)  # 审方系统问题，每次发数据需要时间间隔
        # url = "http://10.1.1.89:9999/auditcenter/api/v1/auditcenter"
        xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', dir_name, xml_name)
        send_data_url = self.conf.get('login', 'address') + '/auditcenter/api/v1/auditcenter'
        headers = {"Content-Type": "text/plain"}
        print(xml_path)
        with open(xml_path, encoding="utf-8") as fp:
            body = fp.read()
        ss = body
        for k in change:
            ss = ss.replace(k, change[k])
        print(ss)
        return self.session.post(url=send_data_url, data=ss.encode("utf-8"), headers=headers)

    def doc(self, dir_name, xml_name, **change):
        xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', dir_name, xml_name)
        url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '医生双签')
        headers = {"Content-Type": "text/plain"}
        print(xml_path)
        with open(xml_path, encoding="utf-8") as fp:
            body = fp.read()
        ss = body
        for k in change:
            ss = ss.replace(k, change[k])
        print(ss)
        return self.session.post(url=url, data=ss.encode("utf-8"), headers=headers)

    # 查询待审列表，获取引擎id（注意：右侧待审任务只能展示10条，所以10条之外的数据查询不到）
    def get_opt_engineid(self, dir_name, xml_name, num):
        self.send_data(dir_name, xml_name, **self.change_data)
        time.sleep(4)
        # num = re.findall('\d+', xml_name)  # 获取文件名中的数字
        recipeno = 'r' + ''.join(str(num)) + '_' + self.change_data['{{ts}}']
        param = {
            "recipeNo": recipeno
        }
        url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '查询待审门诊任务列表')
        res = self.post_json(url, param)
        # print(res)
        # print(res['data']['optRecipeList'][0]['optRecipe']['id'])
        return res['data']['optRecipeList'][0]['optRecipe']['id']

    # 根据patient_id查询待审列表获取引擎id，count=1时，取该患者第二条数据的engineid,count=2时，取该患者第二条数据的engineid
    def get_ipt_engineid(self, dir_name, xml_name, count):
        self.send_data(dir_name, xml_name, **self.change_data)
        time.sleep(5)
        param = {
            "patientId": self.change_data['{{ts}}']
        }
        url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '查询待审住院任务列表')
        res = self.post_json(url, param)
        print(res)
        engineid = ''
        if count == 1:
            engineid = res['data']['engineInfos'][0]['id']
        elif count == 2:
            engineid = res['data']['engineInfos'][1]['id']
        return engineid

    def opt_audit(self, engineid, audit_type):
        url = ''
        param = {}
        # 处方详情审核通过
        if audit_type == 2:
            url = self.conf.get('auditcenter','address') + self.conf.get('api', '处方详情审核通过')
            param = {
                "optRecipeId": engineid,
                "auditResult": ""
            }
        # 处方详情审核打回
        elif audit_type == 0:
            url = self.conf.get('login', 'address') + '/auditcenter' + self.conf.get('api', '处方详情审核打回')
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回必须修改",
                "operationRecordList": [],
                "messageStatus": 0
            }
        # 处方详情审核打回（可双签）
        elif audit_type == 1:
            url = self.conf.get('login', 'address') + '/auditcenter' + self.conf.get('api', '处方详情审核打回')
            param = {
                "optRecipeId": engineid,
                "auditResult": "打回可双签",
                "operationRecordList": [],
                "messageStatus": 1
            }
        self.post_json(url, param)

    # 待审列表批量通过，audit_type = 1指门急诊，audit_type = 3指住院
    def audit_multi(self, audit_type, *ids):
        url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '待审列表批量通过')
        param = {
            "ids": ids,
            "auditType": audit_type,
            "auditWay": 2
        }
        self.post_json(url, param)

    def ipt_audit(self, gp, engineid, audit_type):
        url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '医嘱详情审核')
        param = ''
        # 医嘱详情审核打回
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
        # 医嘱详情审核打回（可双签）
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
        # 医嘱详情审核通过
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
        self.post_json(url, param)

    def get_ipt_patient(self,engineid,type):
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '待审住院获取患者信息') + '?id='+ str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '已审住院获取患者信息') + '?id=' + str(engineid)
        return self.get(url)

    def get_ipt_orderlist(self,engineid,type):
        if type == 0:
            url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '待审住院获取药嘱信息') + '?id='+ str(engineid)
        else:
            url = self.conf.get('auditcenter', 'address') + self.conf.get('api', '已审住院获取药嘱信息') + '?id=' + str(engineid)
        return self.get(url)











if __name__ == '__main__':
    t = Template()
    ids = [99098]
    t.audit_multi(1, *ids)
