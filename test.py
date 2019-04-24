#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def test_a(a=1, b=2, c=3):
    print(a, b, c)


def test_b(**args):
    a = args
    print(args)
    test_a(**a)


test_b(a=4, b=5)
