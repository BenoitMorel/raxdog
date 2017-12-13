import os
import sys
import subprocess
import raxdog_install_constants as const

def install_raxml():
  os.chdir(const.RAXML_PATH)
  try:
    os.mkdir("build")
  except OSError:
    pass
  os.chdir("build")
  subprocess.check_call(["cmake", '-DUSE_MPI=ON', ".."])
  subprocess.check_call(["make"])



install_raxml()
