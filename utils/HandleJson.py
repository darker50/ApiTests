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

    def __init__(self, sessions_path):
        self.sessions_path = sessions_path

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

if __name__ == "__main__":
    h = HandleJson("454")
