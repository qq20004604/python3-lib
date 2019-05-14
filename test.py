#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class A(object):
    def __init__(self):
        self._value = 1
        self._a = 10

    # 获取值
    @property
    def value(self):
        return self._value

    # 赋值
    @value.setter
    def value(self, value):
        self._value = value

    # 获取值
    @property
    def valuea(self):
        return self._a

    # 赋值
    @valuea.setter
    def valuea(self, value):
        self._a = value


a = A()
print(a.value)
a.value = 2
print(a.value)

print(a.valuea)
a.valuea = 11
print(a.valuea)
