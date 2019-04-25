#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request


class RequestTool:
    def __init__(self, url):
        self.url = url;
        self.body = None
        self.status = None
        self.headers = None

    # 重置请求
    def resetURL(self, url):
        self.url = url;
        self.body = None
        self.status = None
        self.headers = None

    # 设置use-agent
    def setUserAgent(self, agent):
        pass

    # 发起请求
    def sendRequestByGet(self):
        with request.urlopen(self.url) as f:
            self.body = f.read().decode('utf-8')
            # http code，正常为 200
            self.status = f.status
            # 返回内容的header
            self.headers = {}
            for (k, v) in f.getheaders():
                self.headers[k] = v

    # 请求是否成功
    def isRequestOK(self):
        return self.status == 200

    # 获取请求头
    def getHeaders(self):
        return self.headers

    # 获取请求头的某一个字段
    def getHeader(self, key):
        return self.headers[key]

    # 获取请求体
    def getBody(self):
        return self.body
