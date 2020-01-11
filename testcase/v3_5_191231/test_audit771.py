# -*- coding: utf-8 -*-
# @Time : 2019/12/9 15:44
# @Author : wangmengmeng
import pytest


# from pytest_assume.plugin import assume

class TestIpt:
    """住院新开 修改 删除 撤销 停止 退药测试用例 """

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7),
                                                         ('audit771_4', 'audit771_5', 'audit771_6', 7),
                                                         ('audit771_7', 'audit771_8', 'audit771_9', None)])
    def test_ipt_return_drug_0(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱-未审核 测试用例"""
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
        pytest.assume(actual == expected)  # 断言待审页面
        zy.audit_multi(*[engineid])
        res = zy.orderList(engineid, 1)
        actual = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual = i['despensingNum']
                break
        pytest.assume(actual == expected)  # 断言已审页面

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_1', 'audit771_2', 'audit771_3', 7),
                                                         ('audit771_4', 'audit771_5', 'audit771_6', 7),
                                                         ('audit771_7', 'audit771_8', 'audit771_9', None)])
    def test_ipt_return_drug_1(self, zy, xml1, xml2, xml3, expected):
        """退药-药嘱-审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        engineid1 = [zy.get_engineid(1)]
        zy.audit_multi(*engineid1)
        zy.send.send('ipt', xml2, 1)
        zy.send.send('ipt', xml3, 1)
        engineid2 = zy.get_engineid(1)
        res = zy.orderList(engineid2, 0)
        actual = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual = i['despensingNum']
                break
        pytest.assume(actual == expected)  # 断言待审页面
        zy.audit_multi(*[engineid2])
        res = zy.orderList(engineid2, 1)
        actual = None
        for i in res['data'][zy.send.change_data['{{gp}}']]:
            if i['drugName'] == '盐酸多巴胺注射液':
                actual = i['despensingNum']
                break
        pytest.assume(actual == expected)  # 断言已审页面

    # @pytest.mark.skip(reason='just skip')
    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_10', 'audit771_11', 'audit771_12', 1),
                                                         ('audit771_10', 'audit771_13', 'audit771_12', None)])
    def test_ipt_return_drug_2(self, zy, xml1, xml2, xml3, expected):
        """退药-草药嘱-未审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        zy.send.send('ipt', xml2, 1)
        zy.send.send('ipt', xml3, 1)
        engineid = zy.get_engineid(2)
        res = zy.herbOrderList(engineid, 0)
        actual = None
        if res['data']:
            for i in res['data'][0]['itemList']:
                if i['drugName'] == '丹参':
                    actual = i['despensingNum']
                    break
        pytest.assume(actual == expected)  # 断言待审页面
        zy.audit_multi(*[engineid])
        res = zy.herbOrderList(engineid, 1)
        actual = None
        if res['data']:
            for i in res['data'][0]['itemList']:
                if i['drugName'] == '丹参':
                    actual = i['despensingNum']
                    break
        pytest.assume(actual == expected)  # 断言已审页面

    @pytest.mark.parametrize("xml1,xml2,xml3,expected", [('audit771_10', 'audit771_11', 'audit771_12', 1),
                                                         ('audit771_10', 'audit771_13', 'audit771_12', None)])
    def test_ipt_return_drug_3(self, zy, xml1, xml2, xml3, expected):
        """退药-草药嘱-审核 测试用例"""
        zy.send.send('ipt', xml1, 1)
        engineid1 = [zy.get_engineid(1)]
        zy.audit_multi(*engineid1)
        zy.send.send('ipt', xml2, 1)
        zy.send.send('ipt', xml3, 1)
        engineid2 = zy.get_engineid(1)
        res = zy.herbOrderList(engineid2, 0)
        actual = None
        if res['data']:
            for i in res['data'][0]['itemList']:
                if i['drugName'] == '丹参':
                    actual = i['despensingNum']
                    break
        pytest.assume(actual == expected)  # 断言待审页面
        zy.audit_multi(*[engineid2])
        res = zy.herbOrderList(engineid2, 1)
        actual = None
        if res['data']:
            for i in res['data'][0]['itemList']:
                if i['drugName'] == '丹参':
                    actual = i['despensingNum']
                    break
        pytest.assume(actual == expected)  # 断言已审页面


class TestOpt:
    """门诊新开 修改 删除作废 退药退费测试用例"""

    def test_new_01(self):
        pass

    def test_new_02(self):
        pass

    def test_modify_01(self):
        pass

    @pytest.mark.parametrize("xmlname,expect")
    def test_del_01(self, mz, xmlname, expect):
        """删除作废单个处方"""
        mz.send.send()  # 开具处方
        mz.send.send()  # 删除作废处方
        mz.send.send()  # 再次开具处方

    def test_del_02(self):
        """删除作废两个处方"""
        pass

    def test_return_01(self):
        pass
