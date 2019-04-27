# 说明

## 1、简介

一个简单的 Web Server。

支持路由处理（见代码），以及当路由未匹配到时，尝试匹配静态文件（目前仅限html）。

## 2、版本迭代

第一版：无论什么路径，返回固定内容

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server


def application(environ, start_response):
	# 用户访问的路径
	print(environ['PATH_INFO'])
	start_response('200 OK', [('Content-Type', 'text/html')])
	return [b"<h3>You are logged.</h3>"]


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
```

第二版：支持一定程度的路由配置


```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server

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
		return result
	else:
	    return [b"<h3>Not Found.</h3>"]


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
```

第三版：当前版本