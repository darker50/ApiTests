#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Retry.py
# Author: HeyNiu
# Created Time: 20160809
"""
重试机制 >> 默认3次
1.接口全部遍历后，读取遍历后数据，取出已经遍历的接口名
2.读取遍历前的全部接口名，与第一步的数据求diff
3.diff接口再从遍历前的接口中取数据，重新遍历
4.重试以上步骤，直到diff不存在或重试次数用完
5.得到最后的数据，生成report
"""
import threadpool
import utils.GlobalList
import utils.FileUtil
import sessions.Request
import sessions.ReadSessions


def retry11(retry=3):
    """
    重试机制，默认3次
    :param retry: 重试次数
    :return:
    """
    r1 = Retry(retry)
    if len(r1.get_diff()) > 0:
        print('发现diff接口，重试机制启动...')
        r1.retry1()


class Retry(object):

    def __init__(self, retry):
        self.retry = retry
        self.after_normal_sessions_path = '%s%s%s' % (utils.GlobalList.SESSIONS_PATH, "\\Sessions\\", utils.GlobalList.HOST)

    def __get_normal_after_sessions(self):
        """
        获取遍历后正常（接口通过）的接口列表
        :return:
        """
        return utils.FileUtil.get_file_list(self.after_normal_sessions_path)

    def __get_not_normal_after_sessions(self):
        """
        获取需要人工验证的接口VerifyRequest
        :return:
        """
        return self.__get_check_after_sessions('VerifyRequest')

    def __get_crash_after_sessions(self):
        """
        获取程序异常接口ProgramCrash，不加入重试机制，直接从diff中剔除
        :return:
        """
        return self.__get_check_after_sessions('ProgramCrash')

    def __get_check_after_sessions(self, sessions_type):
        """
        获取需要检查的接口列表，已去重
        :param sessions_type:
        :return:
        """
        path = '%s%s%s%s' % (self.after_normal_sessions_path, '\\Check\\', sessions_type, '.txt')
        try:
            l = open(path, encoding='utf-8').readlines()
            sessions1 = ('%s%s' % (i.replace('\n', '')[::-1].split('/', 1)[0][::-1], '.txt') for i in l if i.startswith('Request url: '))
            return list(set(sessions1))
        except FileNotFoundError:
            return ()

    def get_diff(self):
        """
        获取diff接口
        diff 接口包含类型
        1.response 响应码 非200的接口
        2.请求超时的接口
        3.其他未知情况的接口（如 代码异常导致）
        :return:
        """
        before_sessions = utils.GlobalList.BEFORE_SESSIONS
        after_sessions = []
        after_sessions.extend(self.__get_normal_after_sessions())
        after_sessions.extend(self.__get_not_normal_after_sessions())
        after_sessions.extend(self.__get_crash_after_sessions())
        return list(set(before_sessions).difference(set(after_sessions)))

    def __get_diff_sessions(self):
        """
        从本地磁盘读取diff接口sessions(request url; request header; ...)
        pass: 一个接口多条session
        :return:
        """
        diff = self.get_diff()
        for d in diff:
            yield sessions.ReadSessions.ReadSessions().get_single_session(d)

    def __will_request_sessions(self):
        """
        将要重跑的sessions，把多个接口的多个session合并为一个列表
        :return:
        """
        s = self.__get_diff_sessions()
        for i in s:
            for j in i:
                yield j

    def __request_sessions(self):
        """
        请求接口
        :return:
        """
        s = self.__will_request_sessions()
        pool = threadpool.ThreadPool(8)
        requests1 = threadpool.makeRequests(sessions.Request.Request().thread_pool, s)
        [pool.putRequest(req) for req in requests1]
        pool.wait()

    def retry1(self):
        """
        重试的接口类型
        1.response 响应码 非200的接口
        2.请求超时的接口
        3.其他未知情况的接口（如 代码异常导致）
        注意：已经知道失败的接口不会再重试，目前是这样考虑的
        :return:
        """
        temp = self.retry
        while self.retry > 0:
            self.retry -= 1
            # 请求接口
            self.__request_sessions()
            print('%s%s' % ('重试中...', temp - self.retry))
            # 再次求差异化文件，还有diff继续，否则停止
            if len(self.get_diff()) > 0:
                print('发现还有diff continue')
                continue
            else:
                break
        print('重试完毕！准备生成报告...')

if __name__ == "__main__":
    r = Retry(3)
