#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName ReadConf.py
# Author: HeyNiu
# Created Time: 20160730
"""
读取配置文件
"""

import os
import utils.GlobalList


class ReadConf(object):

    def __init__(self, conf_path):
        """
        初始化字典
        :param conf_path:
        """
        self.conf_path = conf_path
        self.conf = {'tester': '', 'project': '', 'versionName': '', 'versionCode': '', 'AppBuild': '', 'host': '',
                     'systemType': '2', 'DeviceId': 'ffffffff-b3f1-87ad-90ef-ebeb00000000', 'Model': 'MI+4LTE',
                     'DeviceOS': '23', 'Release': '6.0.1', 'getTokenHost': '', 'loginHost': '', 'loginInfo': '',
                     'SessionsPath': '', 'ApiURL': '', 'SpecialSessions': '', 'SessionsPair': ''}

    def get_conf(self):
        """
        配置文件存入字典
        :return:
        """
        if not os.path.exists(self.conf_path):
            print("请确保配置文件存在！")
            return
        if not self.conf_path.endswith('.conf'):
            print("请确保该文件是配置文件！")
            return
        l = open(self.conf_path, encoding='utf-8').readlines()
        for i in l:
            if i.startswith('tester'):
                self.conf['tester'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('project'):
                self.conf['project'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('versionName'):
                self.conf['versionName'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('versionCode'):
                self.conf['versionCode'] = i.split('= ')[-1].replace('\n', '')
                self.conf['AppBuild'] = self.conf['versionCode']
            if i.startswith('host'):
                self.conf['host'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('getTokenHost'):
                self.conf['getTokenHost'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('loginHost'):
                self.conf['loginHost'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('loginInfo'):
                self.conf['loginInfo'] = i.split('= ')[-1].replace('\n', '')
            if i.startswith('SessionsPath'):
                self.conf['SessionsPath'] = i.split('= ')[-1].replace('\n', '')
                utils.GlobalList.SESSIONS_PATH = self.conf['SessionsPath']
            if i.startswith('ApiURL'):
                self.conf['ApiURL'] = i.split('= ')[-1].replace('\n', '')
                utils.GlobalList.API_URL = self.conf['ApiURL']
            if i.startswith('SpecialSessions'):
                self.conf['SpecialSessions'] = i.split('= ')[-1].replace('\n', '')
                utils.GlobalList.SPECIAL_SESSIONS = self.conf['SpecialSessions']
            if i.startswith('SessionsPair'):
                self.conf['SessionsPair'] = i.split('= ')[-1].replace('\n', '')
                utils.GlobalList.SESSIONS_PAIR = self.conf['SessionsPair']

        return self.conf


if __name__ == "__main__":
    r = ReadConf('D:\\Fiddler Sessions\\ApiText.conf')
    r.get_conf()
