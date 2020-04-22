# -*- coding: utf-8 -*-
# @Time : 2020/4/9 10:58
# @Author : wangmengmeng
import pytest


class TestAudit988:
    @pytest.mark.parametrize("xmlname", ['audit988_1', 'audit988_2', 'audit988_3','audit988_4'],
                             ids=["患者信息身高、体重为特殊字符", "生命体征患者信息为特殊字符", "患者信息身高、体重为中文", "生命体征身高、体重为中文"])
    def test_01(self, zy, xmlname):
        zy.send.send('ipt', xmlname, 1)
        assert zy.selNotAuditIptList()['data']['taskNumList'] # 能正常产生待审任务
