#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName ReadSessions.py
# Author: HeyNiu
# Created Time: 20160729
"""
读取录制的所有接口信息
"""

import os

import utils.FileUtil
import utils.GlobalList
import utils.HandleJson


class ReadSessions(object):
    def __init__(self):
        self.sessions_path = '%s%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Api\\", utils.GlobalList.HOST)

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

            # 移除录制异常的接口，即无数据的接口，否则重试时会计算进去
            file_path = '%s%s%s' % (self.sessions_path, '\\', i)
            try:
                if os.path.getsize(file_path) < 100:
                    os.remove(file_path)
            except FileNotFoundError:
                print('%s%s' % (i, '文件不存在'))

    def __ignore_sessions(self):
        """
        忽略删除接口，用于延迟执行
        :return:
        """
        self.__remove_special_files()
        files = list(utils.FileUtil.get_file_list(self.sessions_path))
        for s in utils.GlobalList.DELETE_DICT.keys():
            file_path = '%s%s' % (s, '.txt')
            if file_path in files:
                files.remove(file_path)
        return files

    def get_single_session_full_path(self, path):
        """
        获取单个文件的所有请求（单个请求的url，请求参数，json_dict，响应体）
        :param path: 完整路径
        :return:
        """
        return self.__read_session(path)

    @staticmethod
    def __read_session(path):
        """
        读取session
        :param path: 路径
        :return:
        """
        single_session = []
        total_session = []
        try:
            l1 = open(path, 'r', encoding='utf-8').readlines()
        except UnicodeDecodeError:
            l1 = open(path, 'r', encoding='utf-16-le').readlines()

        for i1 in l1:
            if not i1.startswith("\n"):
                if i1.startswith("Request url: "):
                    single_session.append(i1.split("Request url: ")[-1].replace("\n", ""))
                if i1.startswith("Request body: "):
                    single_session.append(i1.split("Request body: ")[-1].replace("\n", ""))
                if i1.startswith("Response body: "):
                    json_body = i1.split("Response body: ")[-1].replace("\n", "")
                    single_session.append(utils.HandleJson.HandleJson().decode_json(json_body))
                    single_session.append(json_body)
            if i1.startswith("Session end"):
                if len(single_session) == 4 and single_session[0].find(utils.GlobalList.HOST) != -1:
                    total_session.append(single_session)
                single_session = []
        return total_session

    def get_single_session(self, path):
        """
        获取单个文件的所有请求（单个请求的url，请求参数，响应体）
        :param path: 局部路径
        :return:
        """
        file_path = '%s%s%s' % (self.sessions_path, "\\", path)
        return self.__read_session(file_path)

    def __get_all_session(self):
        """
        获取所有请求
        :return:
        """
        files = self.__ignore_sessions()
        utils.GlobalList.BEFORE_SESSIONS.clear()
        for i2 in files:
            utils.GlobalList.BEFORE_SESSIONS.append(i2)
            yield (self.get_single_session(i2))

    def get_will_request_sessions(self):
        sessions = self.__get_all_session()
        for i in sessions:
            for j in i:
                yield j


if __name__ == "__main__":
    r = ReadSessions()
