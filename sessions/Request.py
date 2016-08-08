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
import json
import time
import urllib.request
import requests
import threadpool
import sessions.ReadConf
import sessions.ReadSessions
import sessions.WriteSessions
import utils.CodeUtil
import utils.GlobalList
import utils.HandleJson


class Request(object):
    def __init__(self, dd_type):
        """
        初始化
        """
        # 读取配置文件
        d = utils.GlobalList.get_dd_type(dd_type)
        read = sessions.ReadConf.ReadConf(d.split("|")[0])
        self.conf = read.get_conf()
        self.AUTHORIZATION = "Digest t=\"%s\",SystemType=\"2\",u=\"%s\",r=\"%s\",DeviceId=\"%s\",Model=\"%s\",DeviceOS=\"%s\",Release=\"%s\",VersionName=\"%s\",VersionCode=\"%s\",PushToken=\"\",uId=\"%s\",uName=\"%s\",uPhone=\"%s\",SessionId=\"%s\",uType=\"%s\",bDChannelId=\"%s\",bDUserId=\"%s\",AppBuild=\"%s\",uUID=\"%s\""
        self.AUTHORIZATION_TOKEN = "Digest u=\"app\",r=\"%s\",SystemType=\"%s\",Model=\"%s\",Release=\"%s\",DeviceId=\"%s\",VersionCode=\"%s\",VersionName=\"%s\",AppBuild=\"%s\",PushToken=\"\",DeviceOS=\"%s\",uUID=\"%s\""
        self.AUTHORIZATION_IMAGE_UPLOAD = "Digest u=\"A\", r=\"B\""
        self.session = requests.session()
        self.TOKEN_NAME = ""
        self.TOKEN_VALUE = ""
        self.uId = "0"
        self.head_uid = d.split("|")[-1]
        self.uName = ""
        self.uPhone = ""
        self.SessionId = ""
        self.uType = "0"
        self.uuid = "0"
        self.temp = "C"
        self.time = ""
        self.format_time = '%Y-%m-%d %H:%M:%S'
        self.__get_token_header()
        self.__login_session()
        self.threading_id = 0
        self.url = ""
        self.request_body = ""
        self.data = ""

    def __timestamp(self):
        """
        获取当前时间
        :return:
        """
        return time.strftime(self.format_time, time.localtime(time.time()))

    def __get_token_header(self):
        """
        生成token头部
        :return:
        """
        des = self.__get_token_des()
        arr = (des, self.conf['systemType'], self.conf['Model'], self.conf['Release'], self.conf['DeviceId'],
               self.conf['versionCode'], self.conf['versionName'], self.conf['AppBuild'], self.conf['DeviceOS'], "0")
        authorization = self.AUTHORIZATION_TOKEN % arr
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}
        response = self.session.post(self.conf['getTokenHost'], headers=headers)
        if json.loads(response.text)['StatsCode'] == 200:
            data1 = json.loads(response.text)['Data']
            self.time = data1['Time']
            self.TOKEN_NAME = data1['TokenName']
            self.TOKEN_VALUE = data1['TokenValue']
        else:
            print("GetToken失败，请手动检查")
            utils.HandleJson.HandleJson.print_json(response.text)

    def __login_session(self):
        """
        调用登录接口，这样后面的接口都能正常访问了
        :return:
        """
        url_login = self.conf['loginHost']
        headers = self.__get_session_header(url_login.split('api/')[-1])
        data_login = r'%s' % self.conf['loginInfo']
        response = self.session.post(url_login, headers=headers, data=data_login)
        if json.loads(response.text)['StatsCode'] == 200:
            data1 = json.loads(response.text)['Data']
            self.uId = data1[self.head_uid]
            self.uName = data1['NickName']
            self.uPhone = data1['Phone']
            self.SessionId = data1['Sid']
            self.uType = data1['UserType']
            self.uuid = data1['UID']
        else:
            print("登录失败，请手动检查")
            utils.HandleJson.HandleJson.print_json(response.text)

    def __get_session_header(self, method_name):
        """
        生成session头部
        :return:
        """
        des = self.__get_session_des(method_name)
        arr = (des[1], method_name, des[0], self.conf['DeviceId'], self.conf['Model'], self.conf['Release'],
               self.conf['DeviceOS'], self.conf['versionName'], self.conf['versionCode'],
               self.uId, urllib.request.quote(self.uName), self.uPhone, urllib.request.quote(self.SessionId),
               self.uType, "", "", self.conf['AppBuild'], self.uuid)
        authorization = self.AUTHORIZATION % arr
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}

    def __get_token_des(self):
        """
        生成token密文
        :return:
        """
        m = hashlib.md5()
        m.update(self.temp.encode())
        return m.hexdigest()

    def __get_session_des(self, method_name):
        """
        生成普通请求密文
        :return:
        """
        date = self.__timestamp()
        temp = "%s%s%s%s%s" % (self.TOKEN_NAME, date, "app", method_name, self.TOKEN_VALUE)
        m = hashlib.md5()
        m.update(temp.encode())
        return m.hexdigest(), date

    def post_session(self, url1, method_name, data1=None):
        """
        发送请求并简单校验response，再写入文件
        :return:
        """
        if not url1.startswith("http://"):
            url1 = '%s%s' % ("http://", url1)
        headers = self.__get_session_header(method_name)
        # print("请求接口 >> " + url1)
        try:
            if len(data1) == 0:
                response = self.session.post(url1, headers=headers, timeout=30)
            else:
                data1 = utils.CodeUtil.url_encode(data1)
                response = self.session.post(url1, headers=headers, data=data1, timeout=30)
        except UnicodeEncodeError:
            print('%s%s' % ('url: ',  url1))
            print('%s%s' % ('UnicodeEncodeError request body ', data1))
            return
        except TimeoutError:
            print('%s%s' % ('TimeoutError url: ', url1))
            return

        session = (url1.split("/")[-1], '%s%s' % ("Request url: ", url1), "Request headers: ", str(headers), '%s%s' % ("Request body: ",
                   data1), "Response code: ", str(response.ok), '%s%s' % ("Response body: \n", str(response.text)))

        if not response.ok:
            sessions.WriteSessions.WriteSessions(self.threading_id, "t", self.threading_id, session,
                                                 "ErrorResponse").start()
        elif json.loads(response.text)['StatsCode'] != 200:
            if json.loads(response.text)['Message'].startswith("程序异常"):
                sessions.WriteSessions.WriteSessions(self.threading_id, "t", self.threading_id, session,
                                                     "ProgramCrash").start()
            else:
                sessions.WriteSessions.WriteSessions(self.threading_id, "t", self.threading_id, session,
                                                     "VerifyRequest").start()
        else:
            sessions.WriteSessions.WriteSessions(self.threading_id, "t", self.threading_id, session, "").start()

        self.threading_id += 1
        # utils.HandleJson.HandleJson.print_json(response.text)
        # 验证response参数后面写

    def thread_pool(self, l):
        """
        准备线程池请求接口
        :param l: 接口列表
        :return:
        """
        try:
            self.post_session(l[0], l[0].split("api/")[-1], l[1])
        except IndexError:
            print('%s%s' % ('IndexError url:\n', l[0]))

    def start(self):
        """
        开始请求接口
        :return:
        """
        print("接口请求中，请等待...")
        s = sessions.ReadSessions.ReadSessions()
        l = s.get_will_request_sessions()  # 获取将要请求的所有接口数据

        d1 = datetime.datetime.now()
        pool = threadpool.ThreadPool(8)
        requests1 = threadpool.makeRequests(self.thread_pool, l)
        [pool.putRequest(req) for req in requests1]
        pool.wait()
        d2 = datetime.datetime.now()
        t = d2 - d1
        print("所有接口请求已完成！")
        print("%s %s%s" % ("耗时：", t.seconds, "s"))


if __name__ == "__main__":
    r = Request(1)
    r.start()
