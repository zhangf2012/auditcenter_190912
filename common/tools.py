# -*- coding: utf-8 -*-
# @Time : 2019/8/6 14:37
# @Author : wangmengmeng
import datetime
import time
import random


class Tool:
    @staticmethod
    def get_ymd(d, h):
        """
        获取日期，格式为%Y-%m-%d
        :param d: d可取0（表示当前日期），正（表示当前日期+d天），负（表示当前日期-d天）
        :param h: 可取h0（表示当前日期），正（表示当前时间点+小时），负（表示当前日期-h小时）
        :return:
        """
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d")
        return date

    @staticmethod
    def get_date(d, h):
        """
        获取日期，格式为%Y-%m-%d %H:%M:%S
        :param d:
        :param h:
        :return:
        """
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d %H:%M:%S")
        return date

    @staticmethod
    def get_ts(d, h):
        """
        获取13位时间戳
        :param d:
        :param h:
        :return:
        """
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d %H:%M:%S")
        # ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))  # 获取10位时间戳
        ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S"))) * 1000  # 获取13位时间戳
        return ts

    @staticmethod
    def get_t(d, h):
        """
        获取10位时间戳
        :param d:
        :param h:
        :return:
        """
        date = ((datetime.datetime.now() + datetime.timedelta(days=d)) + datetime.timedelta(hours=h)).strftime(
            "%Y-%m-%d %H:%M:%S")
        # ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))  # 获取10位时间戳
        ts = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S"))) * 1000  # 获取13位时间戳
        return ts

    @staticmethod
    def get_endtoday():
        now = datetime.datetime.now()
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                             microseconds=now.microsecond)
        lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
        return lastToday

    @staticmethod
    def get_random(a, b):
        """
        生成一个指定范围内的整数
        :param a:
        :param b:
        :return:
        """
        return random.randint(a, b)
