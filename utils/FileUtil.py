#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName FileUtil.py
# Author: HeyNiu
# Created Time: 20160809


import os


def get_file_list(sessions_path):
    """
    获取目标地址目录下的文件列表
    :return: 返回标地址目录下的文件列表
    """
    for root, dirs, files in os.walk(sessions_path):
        return (f for f in files)
