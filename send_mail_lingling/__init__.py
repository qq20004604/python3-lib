#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

# 创建目录
if not os.path.exists('log'):
    os.mkdir('log')


def errlog(msg):
    with open('./log/send-mail-err.log', 'a')as f:
        f.write('%s||%s：%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            sys._getframe(1).f_code.co_name,  # 执行errlog这个函数的函数名字，即上一级函数
            msg
        ))


def log(msg):
    with open('./log/send-mail.log', 'a')as f:
        f.write('%s||%s：%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            sys._getframe(1).f_code.co_name,  # 执行errlog这个函数的函数名字，即上一级函数
            msg
        ))


# 目前遗留问题
# 1、发件人是乱码，
class SendMailTool(object):
    def __init__(self):
        self.sender = 'test'  # 这个似乎没用
        self.receivers = []  # 接收邮件人列表，每个邮箱是一个元素，元素是字符串类型
        self.message = None
        self.content = ''

    # 设置发送者，可选
    def set_sender(self, sender):
        self.sender = sender

    # 设置接受者的邮箱
    def set_receivers(self, receivers):
        self.receivers = receivers

    # 发送邮件，发生成功返回True
    def set_mail_content(self, header, content, sender="key-value-system"):
        try:
            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
            self.message = MIMEText(content, 'plain', 'utf-8')
            self.content = content

            # 标题
            self.message['Subject'] = Header(header, 'utf-8')

            # 发送者，这里建议不要带第二个参数'utf-8'
            self.message['From'] = Header(sender)
            # 接收者，收件人内容为：测试@qq20004604.localdomain
            self.message['To'] = Header(str(self.receivers), 'utf-8')
        except BaseException as e:
            print(str(e))
            errlog(str(e))
            self.message = None

    def send_mail(self):
        if self.message is None:
            print('success，发送者：%s，接受者：%s，内容:%s\n' % (self.sender, str(self.receivers), self.content))
            errlog('success，发送者：%s，接受者：%s，内容:%s\n' % (self.sender, str(self.receivers), self.content))
            return False
        try:
            so = smtplib.SMTP('localhost')
            so.sendmail(self.sender, self.receivers, self.message.as_string())
            log('success，发送者：%s，接受者：%s，内容:%s\n' % (self.sender, str(self.receivers), self.content))
            return True
        except smtplib.SMTPException as e:
            errlog(str(e))
            errlog('success，发送者：%s，接受者：%s，内容:%s\n' % (self.sender, str(self.receivers), self.content))
            print("Error: 无法发送邮件")
            return False


# 测试和示例代码
if __name__ == '__main__':
    smt = SendMailTool()
    smt.set_receivers(['20004604@qq.com'])
    smt.set_mail_content(header='这里是测试标题', content='这里是正文的内容')
    smt.send_mail()
    # sender = 'from@runoob.com'
    # receivers = ['20004604@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #
    # # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    # message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
    # message['To'] = Header("测试", 'utf-8')  # 接收者
    #
    # subject = 'Python SMTP 邮件测试'
    # message['Subject'] = Header(subject, 'utf-8')
    # smtpObj = smtplib.SMTP('localhost')
    # smtpObj.sendmail(sender, receivers, message.as_string())
