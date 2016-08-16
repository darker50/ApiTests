#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName RemoveSession.py
# Author: HeyNiu
# Created Time: 20160726

"""
1.source_path >> 需要移除的session，从fiddler右键Remove Session form disk中得来
2.target_path >> fiddler自动保存的sessions信息
3.通过source_path得到要删除的url和url的请求时间（唯一）
4.读取target_path的文件，拿url的请求时间与之匹配
5.匹配到的session执行删除
6.重新覆盖target_path的文件
"""

import os
import re


class RemoveSession(object):
    def __init__(self):
        self.source_path = "D:\\Fiddler Sessions\\RemoveSession.txt"
        self.target_path = "D:\\Fiddler Sessions\\Api\\"
        self.t = ""
        self.url = ""
        self.host = ""
        self.target_file_path = ""

    def __get_session(self):
        """
        要知道删除那个session，唯一的标识就是时间，时间是一致的，可以从这里入手
        pass：排除GetToken在外（其session的request body无时间）
        :return: 返回一个session的时间格式和session的url
        """
        # Digest t="2016-07-26 11:10:02"
        reg_t = re.compile(r'Digest t="(.+?)"')
        reg_url = re.compile(r'Request url(.+?)\n')
        try:
            data = open(self.source_path, encoding='utf-16-le').read().replace("", "")
            data1 = open(self.source_path, encoding='utf-16-le').readlines()
        except UnicodeEncodeError:
            data = open(self.source_path, encoding='utf-8').read().replace("", "")
            data1 = open(self.source_path, encoding='utf-8').readlines()
        for i in data1:
            if not i.startswith("\n"):
                if i.startswith("Request url: "):
                    self.host = i.replace("Request url: ", "").split("/", 1)[0]
        self.url = re.findall(reg_url, data)[0].split('/')[-1]
        if self.url.startswith("GetToken"):
            return
        self.t = re.findall(reg_t, data)[0]

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

    def __read_target_file(self):
        """
        读取目标文件
        :return:
        """
        file_name = self.__match_file()
        single_session = []
        total_session = []
        if file_name:
            self.target_file_path = '%s%s%s%s' % (self.target_path, self.host, "\\", file_name[0])
            try:
                l = open(self.target_file_path, encoding='utf-16-le').readlines()
            except UnicodeDecodeError:
                l = open(self.target_file_path, encoding='utf-8').readlines()
            for i in l:
                single_session.append(i)
                if i.startswith("Session end"):
                    total_session.append(single_session)
                    single_session = []
        return total_session

    def __remove_session(self):
        """
        移除对应的session，通过前面匹配到的时间来对应
        :return:
        """
        l = self.__read_target_file()
        # 待移除的session
        r = []
        for i in l:
            for j in i:
                if j.find(self.t) != -1:
                    r.append(i)
        for i in r:
            l.remove(i)
        return l

    def override_session_file(self):
        """
        把移除了session的目标文件，重新写入文件
        :return:
        """
        l = self.__remove_session()
        with open(self.target_file_path, 'w', encoding='utf-8') as f:
            for i in l:
                for j in i:
                    f.write(j)


if __name__ == "__main__":
    session = RemoveSession()
    session.override_session_file()
