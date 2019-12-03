# -*- coding: utf-8 -*-
# @Time : 2019/8/14 10:38
# @Author : wangmengmeng
import pymysql
from config.read_config import ReadConfig
from common.logger import log


class ConnectDB:
    def __init__(self):
        log.info('start connecting MySQL...')
        try:
            self.conf = ReadConfig()
            self.host = self.conf.get('mysql', 'host')
            self.port = int(self.conf.get('mysql', 'port'))
            self.username = self.conf.get('mysql', 'username')
            self.password = self.conf.get('mysql', 'password')
            self.db_sys = self.conf.get('mysql', 'db_sys')
            self.db_sf_full = self.conf.get('mysql', 'db_sf_full')
        except Exception as e:
            log.error('连接数据库失败\n错误信息如下\n'.format(e))
        else:
            log.info('连接数据库成功')

    def connect(self, dbname):
        return pymysql.Connect(host=self.host, port=self.port, user=self.username, passwd=self.password,
                               database=dbname, charset='utf8')

    def get_cur(self, conn):
        return conn.cursor()

    def execute(self, cur, sql):
        """
        执行没有变量的sql
        :param sql:
        """
        cur.execute(sql)
        return cur.fetchone()  # 返回的是元组

    def execute_pid(self, cur, sql, pid):
        """执行需要传入患者号patient_id的sql"""
        cur.execute(sql, (pid,))
        return cur.fetchone()[0]


if __name__ == '__main__':
    a = ConnectDB()
    conn = a.connect(a.db_sys)
    cur = a.get_cur(conn)
    sql = a.conf.get('sql', 'zoneid')
    res = a.execute(cur, sql)
    print(res[0])
