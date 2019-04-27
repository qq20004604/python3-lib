#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
import os


def getHtml(path):
	text = 'not found'
	with open(path) as f:
		text = f.readlines()
		text = ''.join(text).encode('utf-8')
	return text


def login(path):
	return [b"<h3>You are logged.</h3>"]


def home_path(path):
	text = getHtml('./1.html')
	return [text]


# 静态文件处理
def static_file(path):
	if os.path.isfile("./static" + path):
		print(True)
		return [getHtml("./static" + path)]
	elif os.path.isfile("./static" + path + '.html'):
		return [getHtml("./static" + path + '.html')]
	else:
		print(False)
		return [getHtml('./404.html')]


routing_table = {
	"/": home_path,
	"/a": login
}


def route(path):
	return routing_table[path](path)


def application(environ, start_response):
	# 用户访问的路径
	print(environ['PATH_INFO'])
	start_response('200 OK', [('Content-Type', 'text/html')])
	if environ['PATH_INFO'] in routing_table:
		# 设置，效果一目了然，略
		result = route(environ['PATH_INFO'])
		print('---- application route ----')
		return result
	else:
		print('---- application static ----')
		return static_file(environ['PATH_INFO'])


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
