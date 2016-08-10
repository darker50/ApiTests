#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName ReadSessions.py
# Author: HeyNiu
# Created Time: 20160729
"""
读取录制的所有接口信息
"""


import os
import utils.GlobalList
import utils.FileUtil


class ReadSessions(object):

    def __init__(self):
        self.sessions_path = '%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Api")
        self.__remove_special_files()

    def __remove_special_files(self):
        """
        删除特定的不加入遍历接口的文件
        e.g.
        金钱相关、发文章等在外网的接口
        :return:
        """
        f = utils.FileUtil.get_file_list(self.sessions_path)
        # str数据转换成list
        remove_sessions = eval(utils.GlobalList.SPECIAL_SESSIONS)
        for i in f:
            for j in remove_sessions:
                if i.startswith(j):
                    os.remove('%s%s%s' % (self.sessions_path, "\\", i))

    def get_single_session(self, path):
        """
        获取单个文件的所有请求（单个请求的url，请求参数，响应体）
        :return:
        """
        single_session = []
        total_session = []
        try:
            l1 = open('%s%s%s' % (self.sessions_path, "\\", path), 'r', encoding='utf-8').readlines()
        except UnicodeDecodeError:
            l1 = open('%s%s%s' % (self.sessions_path, "\\", path), 'r', encoding='utf-16-le').readlines()

        for i1 in l1:
            if not i1.startswith("\n"):
                if i1.startswith("Request url: "):
                    single_session.append(i1.split("Request url: ")[-1].replace("\n", ""))
                if i1.startswith("Request body: "):
                    single_session.append(i1.split("Request body: ")[-1].replace("\n", ""))
                if i1.startswith("Response body: "):
                    single_session.append(i1.split("Response body: ")[-1].replace("\n", ""))
            if i1.startswith("Session end"):
                if len(single_session) == 3:
                    total_session.append(single_session)
                single_session = []
        return total_session

    def __get_all_session(self):
        """
        获取所有请求
        :return:
        """
        files = utils.FileUtil.get_file_list(self.sessions_path)
        for i2 in files:
            yield (self.get_single_session(i2))

    def get_will_request_sessions(self):
        sessions = self.__get_all_session()
        for i in sessions:
            for j in i:
                yield j

if __name__ == "__main__":
    r = ReadSessions()
