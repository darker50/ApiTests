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
JIAZAI_CONF_PATH = '%s%s' % (os.getcwd()[::-1].split('\\', 1)[-1][::-1], '\\ApiTextJiaZai.conf')
DECORATION_CONF_PATH = '%s%s' % (os.getcwd()[::-1].split('\\', 1)[-1][::-1], '\\ApiTextDecoration.conf')
CURRENT_CONF_PATH = ''
SESSIONS_PATH = 'D:\\Fiddler Sessions'
API_URL = 'http://A.B.com/Home/API/BBS'
SPECIAL_SESSIONS = 'GetToken'  # 默认值
SESSIONS_PAIR = ''
CREATE_DICT = {}  # 创建数据接口字典 key >> 接口名 value >> 返回字段id
DELETE_DICT = {}  # 删除接口字典 key >> 接口名 value >> 请求字段id
MAPPING_DICT = {}  # 映射字典，即删除数据接口对应的创建数据接口
HOST = 'A-webapi.test.B.com'
BEFORE_SESSIONS = []  # 遍历前的全部接口，即ReadSessions读取的接口


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
