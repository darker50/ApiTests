#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName HandleJson.py
# Author: HeyNiu
# Created Time: 20160728
"""
处理json信息，用于后面response body字段比较（含字段类型）
"""

import json


class HandleJson(object):
    def __init__(self):
        self.json_list = []

    @staticmethod
    def print_json(json_data):
        """
        以树形结构打印json
        :param json_data: json数据源
        :return:
        """
        try:
            decode = json.loads(json_data)
            print(json.dumps(decode, ensure_ascii=False, sort_keys=True, indent=2))
        except (ValueError, KeyError, TypeError):
            print("JSON format error")

    def decode_json(self, json_data):
        """
        解析json并返回对应的key|value
        :param json_data: json数据源
        :return: 返回json各字段以及字段值
        """
        try:
            data = json.loads(json_data)
        except Exception as e:
            print(e)
            print("JSON format error")
            return []
        self.__iterate_json(data)
        return self.json_list

    def __iterate_json(self, json_data, i=0):
        """
        遍历json
        :param i: 遍历深度
        :param json_data: json数据源
        :return: 返回json各字段以及字段值
        """
        if isinstance(json_data, dict):
            for k in json_data.keys():
                self.json_list.append('%s|%s' % (k, str(type(json_data[k])).split("'")[1]))
                if str(type(json_data[k])).startswith("<class 'list'>"):
                    if len((json_data[k])) and isinstance(json_data[k][0], dict):
                        self.__iterate_json(json_data[k][0], i=i + 1)
                if isinstance(json_data[k], dict):
                    self.__iterate_json(json_data[k], i=i + 1)
        else:
            print("JSON format error")


if __name__ == "__main__":
    h = HandleJson()
