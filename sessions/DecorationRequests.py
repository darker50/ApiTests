#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName DecorationRequests.py
# Author: HeyNiu
# Created Time: 20160812
"""
D request
"""

import difflib
import json
import urllib.request

import base.Request
import sessions.ReadConf
import sessions.WriteSessions
import utils.GlobalList
import utils.HandleJson


class DecorationRequests(base.Request.Request):
    def __init__(self):
        """
        初始化
        """
        super(DecorationRequests, self).__init__()
        # 读取配置文件
        read = sessions.ReadConf.ReadConf(utils.GlobalList.DECORATION_CONF_PATH)
        utils.GlobalList.CURRENT_CONF_PATH = utils.GlobalList.DECORATION_CONF_PATH
        self.conf = read.get_conf()
        self.AUTHORIZATION = "Digest t=\"%s\",SystemType=\"2\",u=\"%s\",r=\"%s\",DevicesId=\"%s\",DeviceId=\"470201315988652\",Model=\"%s\",DeviceOS=\"%s\",Release=\"%s\",VersionName=\"%s\",VersionCode=\"%s\",PushToken=\"\"," \
                             "UserId=\"%s\",UserName=\"%s\",SessionId=\"%s\",bDChannelId=\"%s\",bDUserId=\"%s\",AppBuild=\"%s\""
        self.AUTHORIZATION_TOKEN = "Digest u=\"ABC\",r=\"%s\",SystemType=\"%s\",Model=\"%s\",Release=\"%s\",DevicesId=\"%s\",DeviceId=\"470201315988652\",VersionCode=\"%s\",VersionName=\"%s\",AppBuild=\"%s\",PushToken=\"\",DeviceOS=\"%s\""
        self.__get_token_header()
        self.__login_session()
        self.sessions = ()

    def __get_token_header(self):
        """
        生成token头部
        :return:
        """
        des = self.get_token_des()
        arr = (des, self.conf['systemType'], self.conf['Model'], self.conf['Release'], self.conf['DeviceId'],
               self.conf['versionCode'], self.conf['versionName'], self.conf['AppBuild'], self.conf['DeviceOS'])
        authorization = self.AUTHORIZATION_TOKEN % arr
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}
        response = self.session.post(self.conf['getTokenHost'], headers=headers, data='IsGetAd=true')
        data1 = json.loads(response.text)
        if data1['status'] == 200:
            self.time = data1['time']
            self.TOKEN_NAME = data1['tokenName']
            self.TOKEN_VALUE = data1['tokenValue']
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
        data1 = json.loads(response.text)
        if data1['status'] == 200:
            self.uId = data1['userId']
            self.uName = data1['userName']
            self.SessionId = data1['sessionId']
        else:
            print("登录失败，请手动检查")
            utils.HandleJson.HandleJson.print_json(response.text)

    def __get_session_header(self, method_name):
        """
        生成session头部
        :return:
        """
        des = self.get_session_des(method_name)
        arr = (des[1], method_name, des[0], self.conf['DeviceId'], self.conf['Model'], self.conf['Release'],
               self.conf['DeviceOS'], self.conf['versionName'], self.conf['versionCode'],
               self.uId, urllib.request.quote(self.uName), urllib.request.quote(self.SessionId),
               "4423292378263683538", "661679671330492543", self.conf['AppBuild'])
        authorization = self.AUTHORIZATION % arr
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}

    def __post_request(self):
        """
        请求接口，获得session
        :return:
        """
        # verify response body
        expect_json_body = self.sessions[-1]
        expect_json_list = self.sessions[-2]
        result_json_body = self.sessions[-3]
        result_json_list = utils.HandleJson.HandleJson().decode_json(result_json_body)
        diff = list(set(expect_json_list) ^ (set(result_json_list)))  # 求差集

        if self.sessions[0] != 200:
            sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, self.sessions[1], "ErrorResponse")
        if not diff:
            self.__un_diff_verify_write()
        elif 0.8 < difflib.SequenceMatcher(None, expect_json_list, result_json_list).ratio() < 1.0:
            # 相似度最低限度初定为80%，后续跟进实际情况调整
            # 计算2个list相似度，大于80%小于100%才判断预期，排除大部分数据影响
            self.diff_verify_write(self.sessions[1], expect_json_body, expect_json_list, result_json_body,
                                   result_json_list, diff, "Unexpected")
        elif len(expect_json_list) == len(result_json_list):
            # 长度相等时 主要验证字段类型改变 如：整型变成布尔型
            self.diff_verify_write(self.sessions[1], expect_json_body, expect_json_list, result_json_body,
                                   result_json_list, diff, "FieldChange")
        else:
            # 相似度太低一般由于数据影响，这一块暂不考虑
            self.__un_diff_verify_write()

    def __un_diff_verify_write(self):
        """
        没有差异化以及差异化太大时的验证
        :return:
        """
        status = json.loads(self.sessions[-1])['status']
        if status != 200:
            if json.loads(self.sessions[-1])['msg'].find("异常") != -1:
                sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, self.sessions[1],
                                                      "ProgramCrash")
            else:
                sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, self.sessions[1],
                                                      "VerifyRequest")
        else:
            sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, self.sessions[1], "")

    def post(self, url1, method_name, json_dict, json_body, data1=None):
        """
        请求接口
        :param url1: 请求的url
        :param method_name: 请求的接口名
        :param json_dict: json字典 >> 键值对方式 key：字段 value：字段类型
        :param json_body: 请求返回的response json body
        :param data1: 请求参数
        :return:
        """
        self.sessions = self.post_session(url1, self.__get_session_header(method_name), json_dict, json_body, data1)
        self.__post_request()

    def thread_pool(self, l):
        """
        准备线程池请求接口
        :param l: 接口列表
        :return:
        """
        if l is None or len(l) == 0:
            return
        try:
            self.post(l[0], l[0].split("api/")[-1], l[2], l[-1], l[1])
        except IndexError:
            print('%s%s' % ('IndexError url:\n', l[0]))

    def start(self):
        self.start_thread_pool(self.thread_pool, 3)

if __name__ == '__main__':
    DecorationRequests().start()
