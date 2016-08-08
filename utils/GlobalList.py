#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName GlobalList.py
# Author: HeyNiu
# Created Time: 20160801
"""
接口全局文件
"""


import os


CONF_PATH = '%s%s' % (os.getcwd()[::-1].split('\\', 1)[-1][::-1], '\\ApiText.conf')
BROKER_CONF_PATH = '%s%s' % (os.getcwd()[::-1].split('\\', 1)[-1][::-1], '\\ApiTextBroker.conf')
SESSIONS_PATH = 'D:\\Fiddler Sessions'
API_URL = ''
SPECIAL_SESSIONS = ''
SESSIONS_PAIR = ''
SESSIONS_PAIR_DICT = {}


def get_dd_type(dd_type):
    """
    返回app类型
    :param dd_type: 0 >> A; 1 >> B
    :return:
    """
    d = {0: '%s%s%s' % (CONF_PATH, '|', 'UserId'), 1: '%s%s%s' % (BROKER_CONF_PATH, '|', 'UserID')}
    return d[dd_type]


if __name__ == "__main__":
    print(get_dd_type(1))
