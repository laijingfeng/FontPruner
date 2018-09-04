# !/usr/bin/python
# encoding=utf-8
# version: 2018-06-23 15:58:35
"""
Log模块
"""


import os
import ctypes
import shutil
from datetime import datetime


class Logger(object):
    """
    Log模块
    """

    LEVEL_ERROR = 3
    LEVEL_WARN = 2
    LEVEL_INFO = 1

    COLOR_BLACK = 0  # black.
    COLOR_DARKBLUE = 1  # dark blue.
    COLOR_DARKGREEN = 2  # dark green.
    COLOR_DARKSKYBLUE = 3  # dark skyblue.
    COLOR_DARKRED = 4  # dark red.
    COLOR_DARKPINK = 5  # dark pink.
    COLOR_DARKYELLOW = 6  # dark yellow.
    COLOR_DARKWHITE = 7  # dark white.
    COLOR_DARKGRAY = 8  # dark gray.
    COLOR_BLUE = 9  # blue.
    COLOR_GREEN = 10  # green.
    COLOR_SKYBLUE = 11  # skyblue.
    COLOR_RED = 12  # red.
    COLOR_PINK = 13  # pink.
    COLOR_YELLOW = 14  # yellow.
    COLOR_WHITE = 15  # white.

    foregroundColor = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08\
    , 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    backgroundColor = [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80\
    , 0x90, 0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0]

    def __init__(self, level=LEVEL_INFO, file_path='logger'):
        """
        初始化\n
        level -- 最低打印等级\n
        file_path -- 日志输出文件，不要后缀
        """
        self.__level__ = level
        self.__out_file__ = 1  # 是否输出文件
        self.__file_path__ = file_path

    def __set_cmd_color__(self, color):
        """
        设置控制台颜色\n
        color -- 颜色
        """
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ret = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)
        return ret

    def __set_cmd_default_color__(self):
        """
        设置控制台默认颜色
        """
        self.__set_cmd_color__(self.foregroundColor[self.COLOR_WHITE] | \
        self.backgroundColor[self.COLOR_BLACK])

    def __log__(self, level, content, fore_color=COLOR_WHITE, back_color=COLOR_BLACK):
        """
        打印Log\n
        level -- 日志等级\n
        fore_color -- 字体颜色\n
        back_color -- 背景颜色
        """
        self.__set_cmd_color__(self.foregroundColor[fore_color] | self.backgroundColor[back_color])
        log_info = '{}|{}|{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, content)
        self.__set_cmd_default_color__()

        if self.__out_file__ == 1:
            with open('{}.log'.format(self.__file_path__), 'a') as file_handle:
                file_handle.write('{}\n'.format(log_info))

    def set_config(self, level=LEVEL_INFO, file_path='logger'):
        """
        设置\n
        level -- 最低打印等级\n
        file_path -- 日志输出文件，不要后缀
        """
        self.__level__ = level
        self.__out_file__ = 1
        self.__file_path__ = file_path

    def reset(self):
        """
        重置，日志备份，重新开始写
        """
        if os.path.exists(self.__file_path__ + '.log'):
            shutil.copy(self.__file_path__ + '.log', self.__file_path__ + '-prev.log')
            os.remove(self.__file_path__ + '.log')
        self.__log__('SYS', 'reset log')  # 增加一句系统LOG，避免LOG为空，监听文件没了，同时也好看有响应

    def info(self, content, fore_color=COLOR_WHITE, back_color=COLOR_BLACK):
        """
        普通日志\n
        fore_color -- 字体颜色\n
        back_color -- 背景颜色
        """
        if self.__level__ <= self.LEVEL_INFO:
            self.__log__('INFO', content, fore_color, back_color)

    def warn(self, content, fore_color=COLOR_YELLOW, back_color=COLOR_BLACK):
        """
        警告日志\n
        fore_color -- 字体颜色\n
        back_color -- 背景颜色
        """
        if self.__level__ <= self.LEVEL_WARN:
            self.__log__('WARN', content, fore_color, back_color)

    def error(self, content, fore_color=COLOR_RED, back_color=COLOR_BLACK):
        """
        错误日志\n
        fore_color -- 字体颜色\n
        back_color -- 背景颜色
        """
        if self.__level__ <= self.LEVEL_ERROR:
            self.__log__('ERROR', content, fore_color, back_color)
