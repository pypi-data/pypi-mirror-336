import os
import shutil
from wjj.path import find_files

def copyfile(srcfile, dstpath):  # 子函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        shutil.copy(srcfile, os.path.join(dstpath, fname))  # 复制文件

def copy_deep_shortname(rootpath, shotnamelist, copypath):
    file_path = all_files(rootpath)
    for i in file_path:
        filepath, tmpfilename = os.path.split(i)
        shotname, extension = os.path.splitext(tmpfilename)
        if shotname in shotnamelist:
            copyfile(i, copypath)


def delete_deep_shortname(path,shotnamelist):#主函数
    file_path=all_files(path)
    for i in file_path:
        filepath, tmpfilename = os.path.split(i)  # 获取目录，获取文件名
        shotname, extension = os.path.splitext(tmpfilename)  # 获取短名，获取后缀
        if shotname in shotnamelist:
            print("已经删除",i)
            os.remove(i)