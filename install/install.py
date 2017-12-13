import os
import sys
import subprocess
import raxdog_install_constants as const

def build_raxml():
  os.chdir(const.RAXML_PATH)
  try:
    os.mkdir("build")
  except OSError:
    pass
  os.chdir("build")
  subprocess.check_call(["cmake", '-DUSE_MPI=ON', ".."])
  subprocess.check_call(["make"])

def build_boost():
  os.chdir(const.BOOST_PATH)
  #todobenoit: this is not portable
  subprocess.check_call(["./bootstrap.sh"])
  subprocess.check_call(["./b2", "headers", "--with-mpi", "--with-serialization", "--with-graph"])
  subprocess.check_call(["./b2", "--with-mpi", "--with-serialization", "--with-graph"])

#build_raxml()
#build_boost()



