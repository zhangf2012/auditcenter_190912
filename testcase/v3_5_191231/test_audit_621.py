# -*- coding: utf-8 -*-
# @Time : 2019/12/24 15:23
# @Author : wangmengmeng
import pytest



class TestIpt:
    @pytest.mark.parametrize("xml_name,expected",[("audit621_1",0),("audit621_2", 0)])
    def test_pishi_lingyao(self,zy,xml_name,expected):
        """给药途径为皮试或领药，能产生待审任务但是不跑引擎"""
        zy.send.send('ipt',xml_name,1)
        actual = len((zy.waitIptList())[1])
        assert actual == expected

class TestOpt:
    @pytest.mark.parametrize("xml_name,expected",[("audit621_3",0),("audit621_4", 0)])
    def test_pishi_lingyao(self,mz,xml_name,expected):
        """给药途径为皮试或领药，能产生待审任务但是不跑引擎"""
        mz.send.send('opt',xml_name,1)
        actual = len((mz.waitOptList(1))[1])
        assert actual == expected
