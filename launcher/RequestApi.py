#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName RequestApi.py
# Author: HeyNiu
# Created Time: 20160729
"""
运行api测试总入口
"""

import sessions.Request


def launcher_api_test():
    """
    1.获取接口列表
    2.与本地sessions对比
    3.差异化文件，是否继续
    3.1否 继续录制接口
    3.2是 开始跑接口
    :return:
    """
    r = sessions.Request.Request(0)  # 0 >> A    1 >> B
    r.start()


if __name__ == "__main__":
    launcher_api_test()
