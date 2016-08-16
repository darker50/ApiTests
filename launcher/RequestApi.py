#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName RequestApi.py
# Author: HeyNiu
# Created Time: 20160729
"""
运行api测试总入口
"""


def launcher_api_test(app_type):
    """
    请求总入口
    :param app_type: 0 >> A; 1 >> B; 2 >> C; 3 >> D
    :return:
    """
    if app_type == 0:
        import sessions.DongDongRequests
        sessions.DongDongRequests.DongDongRequests(0).start()
    elif app_type == 1:
        import sessions.DongDongRequests
        sessions.DongDongRequests.DongDongRequests(1).start()
    elif app_type == 2:
        import sessions.JiaZaiRequests
        sessions.JiaZaiRequests.JiaZaiRequests().start()
    elif app_type == 3:
        import sessions.DecorationRequests
        sessions.DecorationRequests.DecorationRequests().start()


if __name__ == "__main__":
    print('接口回归测试启动...')
    launcher_api_test(0)
