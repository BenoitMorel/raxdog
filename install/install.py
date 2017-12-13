import os
import sys
import subprocess
import raxdog_install_constants as const

def mkdirnocheck(path):
  try:
    os.mkdir(path)
  except OSError:
    pass


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

def build_bpp(package):
  os.chdir(os.path.join(const.BPP_PATH, "bpp-" + package))
  mkdirnocheck("build")
  os.chdir("build")
  subprocess.check_call(["cmake", "-DCMAKE_INSTALL_PREFIX=" + const.BPP_INSTALL_PATH, ".."])
  subprocess.check_call(["make"])
  subprocess.check_call(["make", "install"])
  
#build_raxml()
#build_boost()
build_bpp("core")
build_bpp("seq")
build_bpp("phyl")



