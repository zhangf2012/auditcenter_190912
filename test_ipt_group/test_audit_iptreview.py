# -*- coding: utf-8 -*-
# @Time : 2020/4/2 16:58
# @Author : wangmengmeng
import pytest
from api.ipt_all import IptAll


class TestAuditIptreview:
    @pytest.mark.parametrize("orderStatus", [None, "0", "1", "2", "3", "5", "91", "90"],
                             ids=["全部", "审核打回", "审核通过", "超时通过", "自动通过", "人工审核", "可双签", "必须修改"])
    def test_query_by_orderStatus(self, orderStatus):
        """按医嘱状态查询"""
        actual = (IptAll().iptList(orderStatus=orderStatus))['data']['recordCount']
        expect = IptAll().sqlvalue_by_orderStatus(orderStatus)
        assert actual == expect
