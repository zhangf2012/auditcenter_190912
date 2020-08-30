# -*- coding: utf-8 -*-
# @Time : 2020/6/16 14:11
# @Author : wangmengmeng
import allure

@allure.link("https://jira.ipharmacare.net/browse/AUDIT-1032")
@allure.feature('一组药开了多个，第二次相同组号发过来修改，直接以新的组替换内容')
class TestAudit1124:
    @allure.story('同组号减少一个药')
    def test_01(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_2', 1)  # 减少一个药
        zy.send.send('ipt', 'audit771_16', 1)

    @allure.story('同组号只修改药品信息，药品个数不变')
    def test_02(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_3', 1)  # 只修改药品信息，药品个数不变
        zy.send.send('ipt', 'audit771_16', 1)

    @allure.story('同组号增加一个药')
    def test_03(self, zy):
        zy.send.send('ipt', 'audit1124_1', 1)
        zy.send.send('ipt', 'audit1124_4', 1)  # 增加一个药
        zy.send.send('ipt', 'audit771_16', 1)