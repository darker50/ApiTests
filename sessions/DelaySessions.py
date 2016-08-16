#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName DelaySessions.py
# Author: HeyNiu
# Created Time: 20160812
"""
延时执行的sessions
目的：
目的在于避免接口回放创建的数据（如发朋友圈）对外网数据的影响
思路：
通过一个接口对（如：发朋友圈与删除朋友圈），即创建数据与删除数据完成操作
1.配置文件填写创建数据接口名以及response body json中创建数据成功的字段
2.配置文件填写删除数据的接口名以及request body中传入删除数据的字段
3.移除删除接口不加入执行接口列表
4.执行接口请求，请求完毕后读取写入的创建接口数据文件，提取出字段
5.执行接口后提取出删除接口的url request body response body存入list
6.接口执行完毕时遍历创建数据的list，调用相应的删除接口删除数据
"""
import os
import re

import base.Request
import sessions.ReadConf
import sessions.ReadSessions
import utils.FileUtil
import utils.GlobalList


def clear_up(app_type):
    """
    执行清理创建的数据
    :param app_type:
    :return:
    """
    print("清理创建的接口数据...")
    DelaySessions().request_sessions(app_type)


class DelaySessions(object):
    def __init__(self):
        self.create_session_path = '%s%s%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Sessions\\", utils.GlobalList.HOST, "\\")
        self.delete_session_path = '%s%s%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Api\\", utils.GlobalList.HOST, "\\")
        self.create_sessions_parameter_value = self.__get_all_session_create_parameter()

    def __get_single_session_create_parameter(self, session_name):
        """
        获取单个创建数据接口response body json中创建数据成功的字段
        :return:
        """
        total_session = []
        parameter = []
        file_path = '%s%s%s' % (self.create_session_path, session_name, '.txt')
        if os.path.exists(file_path):
            total_session = sessions.ReadSessions.ReadSessions().get_single_session_full_path(
                '%s%s%s' % (self.create_session_path, session_name, '.txt'))
        req = re.compile(r'"%s":[0-9]+' % (utils.GlobalList.CREATE_DICT[session_name], ))
        for i in total_session:
            parameter.append(re.findall(req, i[-1])[0].split(":")[-1])
        return parameter

    def __get_all_session_create_parameter(self):
        """
        获取所有创建数据接口response body json中创建数据成功的字段
        :return:
        """
        create_parameter = {}
        for i in utils.GlobalList.CREATE_DICT.keys():
            create_parameter[i] = self.__get_single_session_create_parameter(i)
        return create_parameter

    def __get_single_session_delete_parameter(self, session_name):
        """
        替换单个删除数据接口request body中传入删除数据的字段值i
        :return:
        """
        total_session = []
        delete_session_name = utils.GlobalList.DELETE_DICT[session_name]
        file_path = '%s%s%s' % (self.delete_session_path, session_name, '.txt')
        if os.path.exists(file_path):
            total_session = sessions.ReadSessions.ReadSessions().get_single_session_full_path(file_path)
        req = re.compile(r'%s=[0-9]+' % (delete_session_name, ))
        for i in total_session:
            if len(i) == 4:
                temp = re.findall(req, i[1])[0].split('=')[-1]
                for j in utils.GlobalList.MAPPING_DICT.keys():
                    if j == session_name:
                        # 匹配对应的创建数据接口
                        create_session_name = utils.GlobalList.MAPPING_DICT[session_name]
                        # 取第一个值，用完删除
                        value = self.create_sessions_parameter_value[create_session_name][0]
                        i = str(i).replace(str(temp), value)  # 替换value
                        l = list(self.create_sessions_parameter_value[create_session_name])
                        l.remove(value)
                        self.create_sessions_parameter_value[create_session_name] = l
                        return eval(i)

    def __get_all_session_delete_parameter(self):
        """
        替换全部删除数据接口request body中传入删除数据的字段值，并返回一个即将请求接口的list
        :return:
        """
        # 根据创建数据接口找到对应的删除接口，并拿出创建数据接口值的长度，多长就调用多少次对应删除接口
        for i in self.create_sessions_parameter_value.keys():
            for j in utils.GlobalList.MAPPING_DICT.keys():
                if utils.GlobalList.MAPPING_DICT[j] == i:
                    for k in range(1, len(self.create_sessions_parameter_value[i]) + 1):
                        # 此处可优化 目前会读取多次文件
                        yield self.__get_single_session_delete_parameter(j)

    def request_sessions(self, app_type):
        """
        请求删除接口
        :return:
        """
        s = self.__get_all_session_delete_parameter()
        base.Request.thread_pool(app_type, s)
        print("接口数据清理完成！")


if __name__ == '__main__':
    print(clear_up(0))
