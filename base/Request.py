#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Request.py
# Author: HeyNiu
# Created Time: 20160728
"""
请求接口核心文件
"""

import datetime
import hashlib

import requests
import threadpool

import retry.Retry
import sessions.DelaySessions
import sessions.ReadSessions
import sessions.WriteSessions
import utils.CodeUtil
import utils.TimeUtil


def thread_pool(app_type, sessions1):
    """
    线程池，根据app类型进行请求
    :param app_type: app类型
    :param sessions1: 请求list
    :return:
    """
    requests1 = []
    pool = threadpool.ThreadPool(8)
    if app_type == 0:
        import sessions.DongDongRequests
        requests1 = threadpool.makeRequests(sessions.DongDongRequests.DongDongRequests(0).thread_pool, sessions1)
    elif app_type == 1:
        import sessions.DongDongRequests
        requests1 = threadpool.makeRequests(sessions.DongDongRequests.DongDongRequests(1).thread_pool, sessions1)
    elif app_type == 2:
        import sessions.JiaZaiRequests
        requests1 = threadpool.makeRequests(sessions.JiaZaiRequests.JiaZaiRequests().thread_pool, sessions1)
    elif app_type == 3:
        import sessions.DecorationRequests
        requests1 = threadpool.makeRequests(sessions.DecorationRequests.DecorationRequests().thread_pool, sessions1)
    [pool.putRequest(req) for req in requests1]
    pool.wait()


class Request(object):
    def __init__(self, thread_count=8):
        """
        初始化
        """
        self.thread_count = thread_count
        self.AUTHORIZATION_IMAGE_UPLOAD = "Digest u=\"A\", r=\"6Fef07d7dc9ac7T5474775e8d24ee293\""
        self.session = requests.session()
        self.TOKEN_NAME = ""
        self.TOKEN_VALUE = ""
        self.uId = "0"
        self.uName = ""
        self.uPhone = ""
        self.SessionId = ""
        self.uType = "0"
        self.temp = "ABC"
        self.time = ""
        self.format_time = '%Y-%m-%d %H:%M:%S'
        self.threading_id = 0

    def get_token_des(self):
        """
        生成token密文
        :return:
        """
        m = hashlib.md5()
        m.update(self.temp.encode())
        return m.hexdigest()

    def get_session_des(self, method_name):
        """
        生成普通请求密文
        :return:
        """
        date = utils.TimeUtil.timestamp(self.format_time)
        temp = "%s%s%s%s%s" % (self.TOKEN_NAME, date, "BCA", method_name, self.TOKEN_VALUE)
        m = hashlib.md5()
        m.update(temp.encode())
        return m.hexdigest(), date

    def diff_verify_write(self, sessions1, expect_json_body, expect_json_list, result_json_body, result_json_list, diff, session_name):
        """
        主要用于差异化写入文件
        :param sessions1: 请求返回的session
        :param expect_json_body: 预期json body
        :param expect_json_list: 预期json list
        :param result_json_body: 实际json body
        :param result_json_list: 实际json list
        :param diff: 差异化list
        :param session_name: 保存session的文件名
        :return:
        """
        sessions1.append('Expect json body: %s' % (expect_json_body,))
        sessions1.append('Expect json dict: %s' % (expect_json_list,))
        sessions1.append('Result json body: %s' % (result_json_body,))
        sessions1.append('Result json dict: %s' % (result_json_list,))
        sessions1.append('Diff: %s' % (diff,))
        sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1, session_name)

    def post_session(self, url1, headers, json_dict, json_body, data1=None):
        """
        发送请求并简单校验response，再写入文件
        :param url1: 请求的url
        :param headers: 请求头
        :param json_dict: json字典 >> 键值对方式 key：字段 value：字段类型
        :param json_body: 请求返回的response json body
        :param data1: 请求参数
        :return:
        """
        if not url1.startswith("http://"):
            url1 = '%s%s' % ("http://", url1)
        try:
            if len(data1) == 0:
                response = self.session.post(url1, headers=headers, timeout=30)
            else:
                data1 = utils.CodeUtil.url_encode(data1)
                response = self.session.post(url1, headers=headers, data=data1, timeout=30)
        except UnicodeEncodeError:
            print('%s%s' % ('url: ', url1))
            print('%s%s' % ('UnicodeEncodeError request body ', data1))
            return ()
        except TimeoutError:
            print('%s%s' % ('TimeoutError url: ', url1))
            return ()
        except requests.ConnectionError as e:
            print('%s%s' % ('ConnectionError url: ', url1))
            print(e)
            return ()
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url1))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url1))
            print(e)
            return ()
        self.threading_id += 1
        return (response.status_code, [url1.split("/")[-1], '%s%s' % ("Request url: ", url1), "Request headers: ", str(headers),
                '%s%s' % ("Request body: ", data1), '%s%s' % ("Response code: ", response.status_code),
                '%s%s' % ("Response body: ", response.text)], response.text, json_dict, json_body)

    def start_thread_pool(self, thread_pool, app_type):
        """
        开始请求接口
        :param thread_pool: 线程池
        :param app_type: 0 >> A; 1 >> B; 2 >> C; 3 >> D
        :return:
        """
        d1 = datetime.datetime.now()
        print("读取接口数据中...")
        s = sessions.ReadSessions.ReadSessions()
        l = s.get_will_request_sessions()  # 获取将要请求的所有接口数据
        print("接口请求中，请等待...")

        pool = threadpool.ThreadPool(self.thread_count)
        requests1 = threadpool.makeRequests(thread_pool, l)
        [pool.putRequest(req) for req in requests1]
        pool.wait()
        print("接口请求完成！")

        # 重试机制
        retry.Retry.retry11(app_type)

        # 清理数据
        print("正在整理创建的数据...")
        sessions.DelaySessions.clear_up(0)
        print("测试报告准备中...")
        d2 = datetime.datetime.now()
        t = d2 - d1
        print('接口回归测试完成！')
        print("%s %s%s" % ("耗时：", t.seconds, "s"))
