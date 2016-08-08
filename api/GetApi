#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName GetApi.py
# Author: HeyNiu
# Created Time: 20160726
"""
从指定url拉取api存入本地
"""

import urllib.request
import re
import datetime
import utils.GlobalList


class GetApi(object):

    def __init__(self):
        """
        初始化
        """
        print("正在连接指定网址......")
        self.startData = datetime.datetime.now()
        self.Url = utils.GlobalList.API_URL
        self.path = '%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\api.txt")

    def __get_html(self):
        """
        获得指定url的html
        :return: 返回一个byte流html
        """
        return urllib.request.urlopen(self.Url).read()

    def __get_api(self):
        """
        通过正则表达式匹配相应的接口
        :return: 返回一个匹配后的接口列表
        """
        html = self.__get_html()
        print("接口拉取成功")
        reg = re.compile(r'<a href="(.+?)" title="(.+?)">(.+?)</a>')
        return re.findall(reg, html.decode('utf-8'))

    def __remove_deprecated_api(self):
        """
        移除一些过期的接口
        :return: 返回一个客户端正在使用的接口列表
        """
        api = self.__clear_api()
        print("移除过期接口......")
        return (index for index in api if index[1].find("已取消") == -1 and index[0].find("已取消") == -1
                and index[1].find("XMPP") == -1 and index[0].find("已不用") == -1 and index[0].find("已失效") == -1
                and index[1].find("废弃") == -1)

    def __clear_api(self):
        """
        去除部分匹配出来是非接口的数据
        :return: 返回一个真正的接口列表，里面包含过期接口，需要进一步移除
        """
        api = self.__get_api()
        print("接口清洗中......")
        return (index for index in api if index[0].startswith(utils.GlobalList.API_URL.split('API')[-1]))

    def __write_file(self, path):
        """
        接口数据写入文件
        :return:
        """
        api = self.__remove_deprecated_api()
        print("接口数据写入文件中......")
        with open(path, 'w') as f:
            for i in api:
                f.write(i[-1].split("/")[-1])
                f.write("\n")
        print("接口数据写入成功")

    def get_api_data(self):
        """
        暴露的外部接口，从服务器拉取接口数据
        :return:
        """
        print("接口拉取中......")
        self.__write_file(self.path)


if __name__ == "__main__":
    api1 = GetApi()
    api1.get_api_data()
    d2 = datetime.datetime.now()
    time = d2 - api1.startData
    print("%s %s%s" % ("耗时：", time.seconds, "s"))
