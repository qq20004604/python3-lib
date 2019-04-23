#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def dtest(a, b, *c):
    print(a, b, *c)


d = [
    (1, 2, 3),
    (1, 2)
]
for i in d:
    dtest(*i)
