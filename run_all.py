import unittest
import os
from common.HTMLTestReportCN import HTMLTestRunner
import sys

prj_path = os.path.dirname(os.path.abspath(__file__))  # 项目路径
sys.path.append(prj_path)  # 把项目的根目录通过sys.path.append添加为执行时的环境变量
testcase_path = os.path.join(prj_path, 'testcase')  # 测试用例路径
report_file = os.path.join(prj_path, 'report', 'report.html')
suite = unittest.defaultTestLoader.discover(testcase_path)
with open(report_file, 'wb') as f:  # 从配置文件中读取
    HTMLTestRunner(stream=f, title="Api Test", description="测试描述", tester="wangmengmeng").run(suite)
