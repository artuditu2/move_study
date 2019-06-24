#!/usr/bin/env python3.6
#12.04.2019 by Artur Wu
# system rsync of files and linking source and dest and some file logging
# used for managing studies on pacs

import sys
import os
import subprocess
from os.path import join, getsize

def count_files(dirroot = './'):
    """
    Count files in given directory/ies --> sourceDir
    """
    # for root, dirs, files in os.walk(dirroot):
    #     print(root, sum(getsize(join(root, name)) for name in files), "Bytes in:", len(files), "files")
    filescount=0
    for files in os.walk(dirroot,followlinks=False):
        c = int(len(files[2]))
        filescount=filescount + c
    return(filescount)

sourceDirs = sys.argv[1:]
# print(sourceDir)
# sourceDir = ['/home/arturwu/projects/python/2011/4/4', '/home/arturwu/projects/python/2011/4/1', '/home/arturwu/projects/python/2011/4/2']
totalfc = 0
fc = 0
for arg in sourceDirs:
    # if arg == sys.argv[0]:
    #     print("Tego nie liczymy")
    # else:
    if os.path.islink(arg):
        print("To link")
    else:
        fc = count_files(arg)
        totalfc += fc
        print("W katalogu:", arg, "jest", fc, "plikow.")

print("Total:", totalfc)
