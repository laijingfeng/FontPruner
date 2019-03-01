# !/usr/bin/python
# encoding=utf-8
# version: 2018-11-13 15:15:00
"""
一些常用小功能
"""

import sys
import os
import stat
import shutil

class JerryUtil(object):
    """
    JerryUtil
    """

    @staticmethod
    def remove_file_or_dir(path):
        """
        删除文件或者目录，支持SVN目录
        """
        if os.path.exists(path) is False:
            return
        if os.path.isfile(path):
            # 修改可写
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        else:
            # 删除子文件夹
            for f in os.listdir(path):
                sf = os.path.join(path, f)
                JerryUtil.remove_file_or_dir(sf)
            shutil.rmtree(path, True, False)
    
    @staticmethod
    def delete_pattern_file(path, pattern1, pattern2=''):
        """
        删除某个目录下符合pattern特征的文件\n
        不递归
        """
        file_list = os.listdir(path)
        for line in file_list:
            file_path = os.path.join(path, line)
            if os.path.isdir(file_path):
                continue
            if line.find(pattern1) != -1:
                if pattern2 != '':
                    if line.find(pattern2) != -1:
                        os.remove(file_path)
                else:
                    os.remove(file_path)

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
    
    @staticmethod
    def get_caller_info():
        """
        获取调用者的信息\n
        文件名，函数名，行号
        """
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return (os.path.basename(f.f_code.co_filename), f.f_code.co_name, f.f_lineno)