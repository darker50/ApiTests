#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName InitFiddler.py
# Author: HeyNiu
# Created Time: 20160809
"""
初始化fiddler文件夹
"""

import os


def create_folder(l1):
    return [os.mkdir(i) for i in l1 if not os.path.exists(i)]


if __name__ == "__main__":
    l = ['D:\\Fiddler Sessions', 'D:\\Fiddler Sessions\\Api', 'D:\\Fiddler Sessions\\Api\\A-webapi.test.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapi.test.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapi.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapi.test.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapi.test.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapi.B.com', 'D:\\Fiddler Sessions\\Api\\A.bbs.B.com',
         'D:\\Fiddler Sessions\\Api\\A.bbs.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapitestv2.outside.B.com',
         'D:\\Fiddler Sessions\\Api\\A-webapiv2.outside.B.com']
    create_folder(l)
