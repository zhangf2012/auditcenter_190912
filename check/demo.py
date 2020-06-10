# -*- coding: utf-8 -*-
# @Time : 2020/3/5 20:38
# @Author : wangmengmeng

import paramiko
import xmltodict

def get_actual_xml():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.1.1.120', 22, 'yyuser', 'iPh@Yyuse2')
    filename = 'eno_1583397621020_pid_1583397621020_20200305163740815.txt'
    stdout = client.exec_command('cat /tmp/hisresult/2020-03-05/H0003/receive_path/{}'.format(filename))[1]
    content = stdout.read()
    print(xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info']['order_status'])
    # print(filenames)



if __name__ == '__main__':
    get_actual_xml()