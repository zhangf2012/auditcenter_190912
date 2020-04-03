# -*- coding: utf-8 -*-
# @Time : 2020/4/2 14:32
# @Author : wangmengmeng
import time
from common.request import HttpRequest
from config.config import *

r = HttpRequest()


def wait(func):
    # func(*args, **kw)可以使函数适配任意多的参数
    def wrapper(*args, **kw):
        time.sleep(3)
        return func(*args, **kw)

    return wrapper


class IptWait:
    @wait
    def selNotAuditIptList(self, patientId=None):
        """查询待审列表"""
        json_data = {
            "patientId": patientId
        }
        return r.http_post(auditcennter_url + "/api/v1/ipt/selNotAuditIptList", json_data).json()


if __name__ == '__main__':
    cc = IptWait()
    print(cc.selNotAuditIptList(1).json())
