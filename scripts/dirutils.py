import os
import shutil

def mkdirnocheck(path):
    try:
        os.mkdir(path)
    except:
        pass

def makedirsnocheck(path):
    try:
        shutil.makedirs(path)
    except:
        pass


