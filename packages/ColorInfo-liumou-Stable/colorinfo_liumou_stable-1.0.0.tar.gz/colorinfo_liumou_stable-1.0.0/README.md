# ColorInfo

## 介绍

ColorInfo 是一个使用Python3编写的简单的彩色日志工具,主要特性:

* 使用简单
* 彩色输出
* 中文注释
* 支持全部Python3版本(>=3.0)


## 安装教程

执行下面的命令即可

```shell
pip3 install --upgrade ColorInfo_liumou_Stable
```

## Demo

```
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-26 23:51
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   演示
"""
from ColorInfo_liumou_Stable import logger，ColorLogger


def demos():
    log = ColorLogger(txt=True, fileinfo=True, basename=False)
    log.info(msg='1', x="23")
    log.error('2', '22', '222')
    log.debug('3', '21')
    log.warning('4', '20', 22)


class Demo:
    def __init__(self):
        self.logger = logger
        self.logger.info("初始化")

    def de(self):
        self.logger.info("de1")
        logger.info("de2")


d = Demo()
d.de()
demos()
```

# 效果

请在`gitee`项目主页查看图片

![logg.png](./Demo.png)

# 项目主页

[https://pypi.org/project/ColorInfo/](https://pypi.org/project/ColorInfo_liumou_Stable/)

[https://gitee.com/liumou_site/ColorInfo.git](https://gitee.com/liumou_site/ColorInfo.git)
