#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName CodeUtil.py
# Author: HeyNiu
# Created Time: 20160729
"""
请求接口返回的信息存入文件，等同于fiddler录制接口保存的信息一致
"""

import re
import urllib.request


def url_encode(s):
    """
    把request body里面的中文编码 >> 目前还有bug，之后再改，如果有2处中文的情况会有问题（只能替换最后一处）
    :param s:\u4E00-\u9FA5\uF900-\uFA2D >> 匹配中文
             \u0391-\uFFE5 双字节编码
    :return:
    """
    r = re.compile(r'[\u4E00-\u9FA5\uF900-\uFA2D\u0391-\uFFE5]+')
    l = re.findall(r, s)
    if len(l) > 0:
        for i in l:
            s = s.replace(i, urllib.request.quote(i))
    return s


if __name__ == "__main__":
    print(url_encode('KeyWord=日哦F可~！@#￥%……&*（）{}|《》？：<《》＆&PageSize=15'))
