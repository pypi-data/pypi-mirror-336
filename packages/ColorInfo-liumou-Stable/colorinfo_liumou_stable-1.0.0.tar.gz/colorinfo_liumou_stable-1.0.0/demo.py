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
from ColorInfo import ColorLogger, logger


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


if __name__ == "__main__":
    d = Demo()
    d.de()
    demos()
