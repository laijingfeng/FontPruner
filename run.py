# !/usr/bin/python
# encoding=utf-8
# version: 2019-03-01
"""
字库整理
"""

import sys
import os
import shutil
from logger import Logger
from jerry_util import JerryUtil
from main_class import MainClass

class WorkClass(MainClass):
    def __init__(self):
        MainClass.__init__(self)

        # 根据需要重新指定配置文件的路径
        self.log_path = './work'  # 日志文件名
        self.log_to_screen = True

        self.config_path = './config.json'  # 配置路径
    
    def work(self):
        """
        实际工作逻辑\n
        覆盖父类
        """
        self.logger.info('==开始==')

        self.work_clean()
        self.work_doing()
        self.work_post()

        self.logger.info('==完成==')
    
    def work_clean(self):
        """
        清理
        """
        output_ttf_dir = os.path.join(self.get_exe_path('./'), './output/output/fonts/')
        JerryUtil.remove_file_or_dir(output_ttf_dir)
        if os.path.exists(output_ttf_dir) is False:
            os.makedirs(output_ttf_dir)
    
    def work_doing(self):
        """
        工作中
        """
        args = ['python', 'FontPruner.py']
        MainClass.execute_shell_command(args)

    def work_post(self):
        """
        后续
        """
        font_path_from = os.path.join(self.get_exe_path('./'), './output/output/fonts/')
        font_path_to = os.path.join(self.get_exe_path('./'), './output_final/')
        font_list = os.listdir(font_path_from)
        for line in font_list:
            file_path = os.path.join(font_path_from, line)
            if os.path.isdir(file_path):
                continue
            if line.find('.ttf') != -1:
                shutil.copy(file_path, font_path_to + line)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
