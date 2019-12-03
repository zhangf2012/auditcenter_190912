# -*- coding: utf-8 -*-
# @Time : 2019/10/31 11:31
# @Author : wangmengmeng
from common.request import HttpRequest
from config.read_config import ReadConfig


class AlterConfig:

    def __init__(self):
        self.conf = ReadConfig()
        self.request = HttpRequest()

    def alter_sys_config(self, id, value):
        url = self.conf.get('login', 'address') + '/syscenter/api/v1/config/updateConfig?id=' + str(id) + '&type=input'
        data = value
        response = self.request.put(url, data).json()
        print(response)

    def alter_default_setting(self, id, code, name, is_use, value):
        url = self.conf.get('login', 'address') + '/syscenter/api/v1/config/updateDefaultSetting'
        data = {
            "id": id,
            "settingCode": code,
            "settingName": name,
            "value": value,
            "valueType": None,
            "remark": None,
            "isUse": is_use,
            "systemCode": None,
            "zoneId": None,
            "typeData": "checkbox"
        }
        print('data', data)
        response = self.request.put(url, data).json()
        print('response', response)


if __name__ == '__main__':
    ac = AlterConfig()
    ac.alter_sys_config(40003, 1)
    ac.alter_default_setting(87,'whether_dialysis', '是否透析',1,1)
