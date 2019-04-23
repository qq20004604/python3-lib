#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


# 重命名
def rename_file(lastname, newname):
    os.rename(lastname, newname)


# 删除文件
def delete_file(filename):
    try:
        os.remove(filename)
    except BaseException as e:
        pass
    finally:
        pass


# 创建目录
def mkdir(filename):
    os.mkdir(filename)


# 删除目录（空文件夹）
def delete_dir(dirname):
    os.rmdir(dirname)
