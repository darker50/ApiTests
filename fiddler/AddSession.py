#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName AddSession.py
# Author: HeyNiu
# Created Time: 20160801
"""
此py文件供fiddler手动添加录制失败的接口
"""

import os


class AddSession(object):
    def __init__(self):
        self.source_path = "D:\\Fiddler Sessions\\AddSession.txt"
        self.target_path = "D:\\Fiddler Sessions\\Api\\"
        self.url = ""
        self.host = ''
        self.session = []
        self.target_file_path = ""

    def __get_session(self):
        """
        获取待添加的session
        :return:
        """
        l = open(self.source_path, encoding='utf-16-le').readlines()
        for i in l:
            if not i.startswith("\n"):
                if i.startswith("Request url: "):
                    self.url = i.split("/")[-1].replace("\n", "")
                    self.host = i.replace("Request url: ", "").split("/", 1)[0]
                    self.session = l
                    return

    def __get_file_list(self):
        """
        获取目标地址目录下的文件列表
        :return: 返回标地址目录下的文件列表
        """
        for root, dirs, files in os.walk("%s%s" % (self.target_path, self.host)):
            return (f for f in files)

    def __match_file(self):
        """
        url与文件列表匹配
        :return:返回匹配的文件
        """
        self.__get_session()
        return [i for i in self.__get_file_list() if i.startswith(self.url)]

    def __write_file(self):
        """
        写文件
        :return:
        """
        try:
            with open(self.target_file_path, 'a', encoding='utf-16-le') as f:
                for i in self.session:
                    f.write(i)
        except UnicodeEncodeError:
            with open(self.target_file_path, 'a', encoding='utf-8') as f:
                for i in self.session:
                    f.write(i)

    def append_session_file(self):
        """
        把session追加到文件
        :return:
        """
        file_name = self.__match_file()
        if file_name:
            self.target_file_path = '%s%s%s%s' % (self.target_path, self.host, "\\", file_name[0])
            self.__write_file()
        else:
            self.target_file_path = '%s%s%s%s%s' % (self.target_path, self.host, "\\", self.url, ".txt")
            self.__write_file()


if __name__ == "__main__":
    session = AddSession()
    session.append_session_file()
