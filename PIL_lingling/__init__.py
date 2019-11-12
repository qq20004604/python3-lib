#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter
import os
import shutil
from printcolor_lingling import print_testresult


class ImgTool(object):
    # --------------- 【1】读取图片 ---------------
    # 初始化，参数都可选
    def __init__(self, url=None, *img_type):
        # 原图片对象（读取后不会改变）
        self.img = None

        # 处理后的图片对象状态
        self.imgCurrentStatus = None

        # 初始化代码
        if url:
            self.img = Image.open(url, *img_type)
        else:
            self.img = None

    # 读取图片，url必填，类型可选（使用默认的）
    def open_image(self, url, *mode):
        self.img = Image.open(url, *mode)

    # --------------- 【1】读取图片(完) ---------------

    # --------------- 【2】图片备份 ---------------
    # 备份当前图片状态
    def save_img_status(self):
        self.imgCurrentStatus = self.img.copy()

    # 读取之前保存的图片状态
    def load_img_status(self):
        self.img = self.imgCurrentStatus.copy()

    # --------------- 【2】图片备份(完) ---------------

    # --------------- 【3】图片逻辑 ---------------

    # 基于原图产生缩略图（区别：直接修改原图，只能缩小不能放大）
    def thumbnail(self, scale_x, scale_y=None):
        if scale_y == None:
            scale_y = scale_x
        w, h = self.img.size
        w = int(w * scale_x)
        h = int(h * scale_y)
        self.img.thumbnail((w, h))

    # 图片缩放，x、y轴按参数缩放，1表示缩放程度100%
    # 参数2不填写，则x、y等比例缩放
    def img_scale_xy(self, scale_x, scale_y=None):
        if scale_y == None:
            scale_y = scale_x
        w, h = self.img.size
        w = int(w * scale_x)
        h = int(h * scale_y)
        self.img = self.img.resize((w, h))

    # png图片转jpg图片
    # 手动将png保存为png，需要先调用这个函数再调用save_img
    # 也可以直接调用 save_as_jpg 更简单
    def covert_jpg(self):
        self.img = self.img.convert('RGB')

    # 图片模糊，这个测试得手动查看=.=
    def blur_img(self):
        self.img = self.img.filter(ImageFilter.BLUR)

    # 左右反转
    def flip_left_right(self):
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)

    # 旋转
    def rotate(self, deg):
        self.img = self.img.rotate(deg)

    # --------------- 【3】图片逻辑(完) ---------------

    # --------------- 【4】图片状态获取 ---------------

    # 返回当前图片对象
    def get_img(self):
        return self.img

    # 返回当前图片的宽高
    def get_img_size(self):
        return self.img.size

    # --------------- 【4】图片状态获取（完） ---------------

    # ---------- 【5】保存 ----------

    # 保存图片
    # 如果保存为 jpg，建议直接用下面那个
    def save_img(self, img_name, *img_type):
        self.img.save(img_name, *img_type)

    # 转换为jpg格式
    def save_as_jpg(self, img_name):
        self.img = self.img.convert('RGB')
        self.img.save(img_name, 'jpeg')


# 测试代码
if __name__ == '__main__':
    try:
        # 最后再删除文件和文件夹
        if os.path.isdir('test'):
            # 递归删除文件和文件夹
            shutil.rmtree('test')

        img = ImgTool()
        # 读取图片
        img.open_image('01.png')

        # -- png --
        # 保存当前图片状态
        img.save_img_status()
        # 放大2倍
        img.img_scale_xy(2)
        # 判断目录是否存在
        if not os.path.isdir('test'):
            os.makedirs("test")
        # 保存图片(2倍原图大小 png）
        img.save_img('test/02.png')

        # -- jpg --
        # 读取图片状态
        img.load_img_status()
        # 转为jpg
        img.covert_jpg()
        # 缩放0.25倍
        img.img_scale_xy(0.25)
        # 保存图片（0.25倍原图大小 jpg）
        img.save_as_jpg('test/02.jpg')

        # -- 模糊 --
        img.load_img_status()
        img.blur_img()
        img.save_img('test/03.png')

        # -- 左右反转 --
        img.load_img_status()
        img.flip_left_right()
        img.save_img('test/04.png')

        # -- 旋转（deg） --
        img.load_img_status()
        img.rotate(270)
        img.save_img('test/05.png')

        # --- 下来开始测试 ---
        img_test = ImgTool('01.png')
        w, h = img_test.get_img_size()
        img_test.open_image('test/02.png')
        w1, h1 = img_test.get_img_size()
        img_test.open_image('test/02.jpg')
        w2, h2 = img_test.get_img_size()

        print_testresult((w1 == w * 2 and h1 == h * 2 and w2 == int(w * 0.25) and h2 == int(h * 0.25)), 'PIL_lingling')
    except BaseException as e:
        print_testresult(False, 'PIL_lingling')
        print(e)
