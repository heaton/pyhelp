#! /usr/bin/env python
# -*- coding=utf-8 -*-
# python rm.py -d=31 /Users/HeatoN/Downloads/til > delete.log
import sys
import os
import time

dir = "."
day = 31
rmdir = True
# process argv eg: -d=30 .
for arg in sys.argv[1:]:
    if arg.startswith("-d"):
        day = int(arg.split("=")[1])
    elif arg.startswith("-s"):
        rmdir = False
    else:
        dir = arg

now = time.time()

def removeSpaceDir(root):
    for f in os.listdir(root):
        path = os.path.join(root, f)
        if os.path.isdir(path):
            removeSpaceDir(path)
        if len(os.listdir(root))==0:
            os.rmdir(root)
            print "del " + root

for root, dirs, files in os.walk(dir):
    for f in files:
        fpath = os.path.join(root, f)
        fileMtime = os.path.getmtime(fpath)
        fileCtime = os.path.getctime(fpath)
        ld = int((now-max(fileMtime, fileCtime))/3600/24)
        if ld>day:
            print "del " + fpath + " " + str(ld)
            os.remove(fpath)

if rmdir:
    removeSpaceDir(dir)
