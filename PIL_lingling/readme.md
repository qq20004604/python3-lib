# 说明

## 1、作用

PIL模块再包装，用于图片缩放，图片转换格式（png转jpg）等，具体功能不断更新中。

引入方法：

```
from PIL_lingling import ImgTool
```

## 2、使用方法

1. 初始化并打开图片
2. 对图片进行编辑
3. 保存图片


示例：

```
# 1、打开图片
img = ImgTool('01.png')
# 2、编辑图片（例如缩放图片，这里是放大2倍）
img.img_scale_xy(2)
# 3、保存图片
img.save_img('test/02.png')
# 3(2)、以jpg格式保存
img.save_as_jpg('test/02.jpg')
```	

更多示例内容，可以查看源代码中的单元测试部分