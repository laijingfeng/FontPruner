# !/usr/bin/python
# encoding=utf-8
# version: 2020-08-15

from __future__ import print_function
import sys
import os

PY3 = False
enter_cwd_dir = ''
python_file_dir = ''

def execute_shell_command(args, wait='T'):
	p = subprocess.Popen(args)
	if wait == 'T':
		ret = p.wait()
		return ret
	else:
		return 0

def get_exe_path(simple_path):
    """
    相对路径转绝对路径
    """
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)

def process_one_file(filename):
    root_dir = get_exe_path('./')
    input_path = os.path.join(root_dir, filename)
    out_name = '{}.ttf'.format(filename)
    output_path = os.path.join(root_dir, out_name)
    # TODO:.\otfccdump.exe xxx.otf | .\otfccbuild.exe -o xxx.ttf

if __name__ == '__main__':
    if sys.version.startswith('3.'):
        PY3 = True
    else:
        PY3 = False
    
    if PY3 is False:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    enter_cwd_dir = os.getcwd()
    python_file_dir = os.path.dirname(sys.argv[0])

    p = get_exe_path('./')
    files = os.listdir(p)
    for f in files:
        file_path = os.path.join(p, f)
        if os.path.isdir(file_path):
            continue
        if f.endswith('.otf') or f.endswith('.OTF'):
            process_one_file(f)
    print('finish')
