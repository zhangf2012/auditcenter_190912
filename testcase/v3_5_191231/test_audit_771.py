# -*- coding: utf-8 -*-
# @Time : 2019/12/9 15:44
# @Author : wangmengmeng
import pytest


class TestIptReturnDrug:

    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7),
                                                         ('audit771_4', 'audit771_5', 'audit771_6', 7),
                                                         ('audit771_7', 'audit771_8', 'audit771_9', None)])
    def test_ipt_return_drug_0(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱测试用例-未审核"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(2)
        res = zy.orderList(engineid, 0)
        # actual = [i['despensingNum'] for i in res['data'][zy.send.change_data['{{gp}}']] if i['drugName'] == '盐酸多巴胺注射液'][0]
        # actual = [i['despensingNum'] if i['drugName'] == '盐酸多巴胺注射液' else 0 for i in res['data'][zy.send.change_data['{{gp}}']]][0] 这种方法由于actual里存了多个值不好确定我要取哪个
        actual = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual = i['despensingNum']
                break
        assert actual == expected

    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7),
                                                         ('audit771_4', 'audit771_5', 'audit771_6', 7),
                                                         ('audit771_7', 'audit771_8', 'audit771_9', None)])
    def test_ipt_return_drug_1(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱测试用例-审核"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        engineid1 = [zy.get_engineid(1)]
        zy.audit_multi(*engineid1)
        zy.send.send('ipt', xml3, 1)
        engineid2 = zy.get_engineid(1)
        res = zy.orderList(engineid2, 0)
        actual = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual = i['despensingNum']
                break
        assert actual == expected
