# !/usr/bin/python
# encoding=utf-8
# version: 2019-04-29

import sys
import os

SepPath = os.path.sep # 分隔符
InputFilelist = "input_filelist.txt" # 白名单文件列表记录文件
IntermediateFolder = "intermediate" # 白名单汇总目录
OutputFolder = "output" # 新字体输出目录
ChineseOutPut = "ChineseOutPut.txt" # 白名单汇总文件_汉字
UnChineseOutPut = "unChineseOutPut.txt" # 白名单汇总文件_非汉字
Succ = 0

enter_cwd_dir = ''  # 执行路径
python_file_dir = ''  # python文件路径

def get_exe_path(simple_path):
  """
  相对路径转绝对路径
  """
  global enter_cwd_dir
  global python_file_dir
  return os.path.join(enter_cwd_dir, python_file_dir, simple_path)

def genFilePathList(inputPath, FileListOP):
  """
  收集白名单文件列表\n
  inputPath - 白名单目录\n
  FileListOP - 输出临时目录
  """
  print "==收集白名单文件列表 开始=="
  fullPara = ""
  for path in inputPath:
    fullPara += path + " "
  fullPara += " " + FileListOP + SepPath + InputFilelist    
  command = "java -jar {} {}".format(get_exe_path('./bin/GenFileList.jar'), fullPara)
  if os.system(command) is not Succ:
    raise Exception('generate fileList.txt error!'+command)
  print("--收集白名单文件列表 完成--")

def extractFileString(temp):
  """
  白名单内容汇总\n
  temp - 输出临时目录
  """
  print "==白名单内容汇总 开始=="
  fileListPath = temp + SepPath + InputFilelist
  outputPath = temp + SepPath + IntermediateFolder

  command = "java -jar {} {} {}".format(get_exe_path('./bin/fontExtract.jar'), fileListPath, outputPath)
  if os.system(command) is not Succ:
    raise Exception('extract font string  error!'+command)
  print("--白名单内容汇总 完成--")

def bulidNewFont(originPath, outPutPath):
  """
  生成新字体\n
  originPath - 输入字体文件列表\n
  outPutPath - 输出临时目录
  """
  print "==生成新字体 开始=="
  fullOutPut = outPutPath + SepPath + OutputFolder
  if not os.path.exists(fullOutPut):
    os.makedirs(fullOutPut)
  for fontOrigin in originPath:
    index = len(fontOrigin) - fontOrigin.rfind(SepPath)
    fontName = fontOrigin[-index:]
    print ("字体文件：" + fontName)
    fullPara = ""
    fullPara += outPutPath + SepPath + IntermediateFolder + SepPath+ChineseOutPut + "  " + outPutPath + SepPath + IntermediateFolder + SepPath+UnChineseOutPut + " " + fontOrigin + " " + fullOutPut + SepPath + fontName
    command = "java -jar {} -c {}".format(get_exe_path('./bin/sfnttool.jar'), fullPara)
    
    if os.system(command) is not Succ:
      raise Exception('build new font error!'+command)
    
    print("--生成新字体 完成--")

if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  
  enter_cwd_dir = os.getcwd()
  python_file_dir = os.path.dirname(sys.argv[0])

  arguments = {} # 参数列表
  arguments['--inputPath'] = [get_exe_path('./input')] # 白名单目录

  arguments['--inputFont'] = [] # 输入字体文件列表
  font_path = get_exe_path('./fonts/')
  list = os.listdir(font_path)
  for line in list:
    file_path = os.path.join(font_path, line)
    if os.path.isdir(file_path):
        continue
    if line.endswith('.ttf'):
        arguments['--inputFont'].append(file_path)
  
  arguments['--tempPath'] = get_exe_path('./output') # 输出临时目录
  tmp = arguments['--tempPath']

  genFilePathList(arguments['--inputPath'], tmp) 
  print('')
  extractFileString(tmp)
  print('')
  bulidNewFont(arguments['--inputFont'], tmp)