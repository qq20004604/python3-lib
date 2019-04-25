#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 客户端，启动后
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 8000))

print("启动链接")
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))

while True:
    str = input("请输入你要给server端发送的信息：")
    # 防止空输入
    if str == '':
        continue
    print("发送中...")
    # 发送数据:
    s.send(bytes(str, encoding="utf8"))
    rev = s.recv(1024).decode('utf-8')
    print("server端返回：", rev)
    if str == "e" or rev == 'Bye~':
        print("退出中...")
        s.send(b'exit')
        s.close()
        break

print("你已经成功退出链接")
