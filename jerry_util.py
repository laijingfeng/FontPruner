# !/usr/bin/python
# encoding=utf-8
# version: 2018-08-20 10:34:17
"""
一些常用小功能
"""

import sys
import os
import shutil

class JerryUtil(object):
    """
    JerryUtil
    """

    @staticmethod
    def remove_file_or_dir(path):
        """
        删除文件或者目录
        """
        if os.path.exists(path) is False:
            return
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path, True)
    
    @staticmethod
    def copy_dir(src, des):
        """
        拷贝目录
        """
        if os.path.exists(src) is False:
            return
        for f in os.listdir(src):
            src1 = os.path.join(src, f)
            des1 = os.path.join(des, f)
            if os.path.isfile(src1):
                if not os.path.exists(des):
                    os.makedirs(des)
                shutil.copy(src1, des1) 
            if os.path.isdir(src1):
                JerryUtil.copy_dir(src1, des1)