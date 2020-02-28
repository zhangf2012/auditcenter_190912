# -*- coding: utf-8 -*-
# @Time : 2019/12/24 15:23
# @Author : wangmengmeng
import pytest



class TestIpt:
    @pytest.mark.parametrize("xml_name,expected",[("audit621_1",0),("audit621_2", 0)])
    def test_pishi_lingyao(self,zy,xml_name,expected):
        """给药途径为皮试或领药，能产生待审任务但不跑引擎且原本应从引擎取得字段在不跑引擎时审方应自己处理正确"""
        zy.send.send('ipt',xml_name,1)
        actual = len((zy.waitIptList())[1])
        assert actual == expected
        # 断言患者基本信息
        engineid = zy.get_engineid(1)
        patient_data = zy.get_patient(engineid,0)['data']  # 断言待审页面
        assert patient_data['height'] == '120cm'
        assert patient_data['weight'] == '60kg'
        assert patient_data['ccr'] == "90"
        assert patient_data['bsa'] == '1.3471㎡(计算)'
        assert patient_data['pregnancy'] == 1
        assert patient_data['breastFeeding'] == 1
        zy.audit_multi(*[engineid])
        patient_data2 = zy.get_patient(engineid, 1)['data']  # 断言已审页面
        assert patient_data2['height'] == '120cm'
        assert patient_data2['weight'] == '60kg'
        assert patient_data2['ccr'] == "90"
        assert patient_data2['bsa'] == '1.3471㎡(计算)'
        assert patient_data2['pregnancy'] == 1
        assert patient_data2['breastFeeding'] == 1

class TestOpt:
    @pytest.mark.parametrize("xml_name,expected",[("audit621_3",0),("audit621_4", 0)])
    def test_pishi_lingyao(self,mz,xml_name,expected):
        """给药途径为皮试或领药，能产生待审任务但是不跑引擎"""
        mz.send.send('opt',xml_name,1)
        actual = len((mz.waitOptList(1))[1])
        assert actual == expected
        # 断言患者基本信息
        engineid = mz.get_engineid(1)
        patient_data = mz.get_recipeInfo(engineid, 0)['outpatient']  # 断言待审页面
        assert patient_data['height'] == '120cm'
        assert patient_data['weight'] == '60kg'
        assert patient_data['ccr'] == "90.0"
        assert patient_data['bsa'] == '1.3471㎡(计算)'
        assert patient_data['pregnancy'] == 1
        assert patient_data['breastFeeding'] == 1
        mz.audit_multi(*[engineid])
        patient_data2 = mz.get_recipeInfo(engineid, 1)['outpatient']  # 断言已审页面
        assert patient_data2['height'] == '120cm'
        assert patient_data2['weight'] == '60kg'
        assert patient_data2['ccr'] == "90.0"
        assert patient_data2['bsa'] == '1.3471㎡(计算)'
        assert patient_data2['pregnancy'] == 1
        assert patient_data2['breastFeeding'] == 1

