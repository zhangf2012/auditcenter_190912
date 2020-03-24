## 脚本使用说明：
方式一：命令行执行脚本
1.修改pytest.ini，指定要执行的测试用例<br />
2.cmd下进入项目根目录或者通过pycharm的Terminal进入项目根目录，执行pytest命令<br />
等2执行执行结束后再执行3和4<br />
3.cmd下进入项目根目录或者通过pycharm的Terminal进入项目根目录，执行命令allure generate allure-results -o allure-report --clean  生成测试报告<br />
4.进入项目的allure-report目录使用浏览器打开index.html查看测试报告
方式二：
执行运行根目录下的run.py



## 关于测试用例的说明：
审方接收数据有两个接口，对内和对外
1.config.ini里的登录用户不要在药师权限设置页面设置药师权限，否则在查询待审列表时该药师获取不到数据，后续测试用例无法执行
2.如果使用对外接口，接口系统配置需要调整配置-是否开启老版本接口为禁用 状态
3.AUDIT-756是患者模式下的问题，可先不用管
4.AUDIT-771如果使用对外接口，脚本需要做调整
