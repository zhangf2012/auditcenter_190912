# -*- coding: utf-8 -*-
# @Time : 2020/4/14 14:11
# @Author : wangmengmeng
import xmltodict
import pytest
import datetime, time
from pprint import pprint
from common.connect_linux import ConLinux

curdate = ((datetime.datetime.now())).strftime("%Y-%m-%d")  # 获取当天日期
print(curdate)


@pytest.fixture(scope='module', autouse=True)
def get_conn():
    cl = ConLinux()
    yield cl.get_client()


class TestIptAuditresult:
    # 验证落地文件的审核结果
    @pytest.mark.parametrize("xmlname,is_success,status", [('ipt_1', '1', '2')],
                             ids=["待审列表审核通过"])
    def test_01(self, zy, get_conn, xmlname, is_success, status):
        zy.send.send('mainscene', xmlname, 1)
        engineid = zy.get_engineid(1)
        zy.audit_multi(engineid)
        filename = zy.send.change_data['{{ts}}']
        time.sleep(3)
        stdout = get_conn.exec_command('cat /tmp/hisresult/{}}/H0003/IPT/{}/AUDIT_RESULT/OUT_{}*.txt'.format(curdate, filename,filename))[1]
        # stdout = get_conn.exec_command('cat /tmp/hisresult/{}/H0003/return_path/{}*.txt'.format(curdate, filename))[1]
        content = stdout.read()
        # print(xmltodict.parse(content))
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['result']['message']['is_success'] == is_success
        assert xmltodict.parse(content)['root']['result']['message']['status'] == status

    @pytest.mark.parametrize("xmlname,audittype,is_success,status",
                             [('ipt_1', 0, '0', '0'), ('ipt_1', 1, '0', '1'), ('ipt_1', 2, '1', '2')],
                             ids=["审核打回(必须修改)", '审核打回(可双签)', '详情页面审核通过'])
    def test_02(self, zy, get_conn, xmlname, audittype, is_success, status):
        zy.send.send('mainscene', xmlname, 1)
        engineid = zy.get_engineid(1)
        gp = zy.send.change_data['{{gp}}']
        zy.ipt_audit(gp, engineid, audittype)
        filename = zy.send.change_data['{{ts}}']
        time.sleep(3)
        stdout = get_conn.exec_command('cat /tmp/hisresult/{}}/H0003/IPT/{}/AUDIT_RESULT/OUT_{}*.txt'.format(curdate, filename,filename))[1]
        content = stdout.read()
        # print(xmltodict.parse(content))
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['result']['message']['is_success'] == is_success
        assert xmltodict.parse(content)['root']['result']['message']['status'] == status
