#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName TimeUtil.py
# Author: HeyNiu
# Created Time: 20160809


import time


def timestamp(format_time):
    """
    获取当前时间
    :return:
    """
    return time.strftime(format_time, time.localtime(time.time()))
