#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName GetDiffApi.py
# Author: HeyNiu
# Created Time: 20160727
"""
1.通过拿到服务器拉取回来的接口路径与fiddler录制的接口路径
比较，得到差异化文件（未录制的接口文件）
2.录制接口，直到差异化文件接口数为0
"""

import os
import utils.GlobalList


class GetDiffApi(object):

    def __init__(self):
        """
        初始化
        """
        self.api_path = '%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\api.txt")
        self.session_path = '%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Api")

    def __get_api(self):
        """
        从本地获取api列表
        :return:
        """
        if os.path.exists(self.api_path):
            l = open(self.api_path, encoding='gbk').readlines()
            return (index.replace("\n", "") for index in l)

    def __get_sessions_api(self):
        """
        从本地获取已经请求过的sessions
        :return:
        """
        for root, dirs, files in os.walk(self.session_path):
            return (f.split(".")[0] for f in files)

    def __get_diff_api(self):
        """
        求diff
        :return:
        """
        api = self.__get_api()
        sessions_api = self.__get_sessions_api()
        return list(set(api).difference(set(sessions_api)))

    def write_diff_file(self):
        """
        diff写入文件
        :return:
        """
        d = self.__get_diff_api()
        with open(str(self.api_path).replace("api.txt", "diffApi.txt"), 'w', encoding='gbk') as f:
            for i in d:
                f.write(i)
                f.write("\r\n")


if __name__ == "__main__":
    g = GetDiffApi()
    g.write_diff_file()
