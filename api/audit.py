# -*- coding: utf-8 -*-
# @Time : 2020/4/2 14:03
# @Author : wangmengmeng
from common.request import HttpRequest
from config.config import *

r = HttpRequest()


class Audit:
    """审核接口"""

    def auditBatchAgree(self, auditType, *engineids):
        """待审列表批量通过"""
        param = {
            "ids": engineids,
            "auditType": auditType,  # 3指住院 1指门急诊
            "auditWay": 2
        }
        return r.http_post(auditcennter_url + "/api/v1/auditBatchAgree", param)

    def AuditRefuse(self):
        """处方详情审核打回"""
        pass

    def AuditAgree(self):
        """处方详情审核通过"""
        pass

    def auditSingle(self):
        """医嘱详情审核"""
        pass

    def lockDistributeTask(self):
        """查看任务详情时锁定任务"""
        pass

    def unlockDistributeTask(self):
        """退出详情或审核后解除任务锁定"""
        pass

    def startAuditWork(self):
        """开始审方"""
        pass

    def endAuditWork(self):
        """结束审方"""
        pass
