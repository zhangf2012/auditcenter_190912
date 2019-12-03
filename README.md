脚本使用说明：
1.修改pytest.ini，指定要执行的测试用例
2.cmd下进入项目根目录或者通过pycharm的Terminal进入项目根目录，执行pytest命令
等2执行执行结束后再执行3和4
3.cmd下进入项目根目录或者通过pycharm的Terminal进入项目根目录，执行命令allure generate allure-results -o allure-report --clean  生成测试报告
4.进入项目的allure-report目录查看测试报告