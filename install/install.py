import os
import sys
import subprocess
import raxdog_install_constants as const
import shutil
import glob
import time 

def mkdirnocheck(path):
  try:
    os.mkdir(path)
  except OSError:
    pass

def rmnocheck(path):
  try:
    shutil.rmtree(path)
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
  with open(os.path.join(const.BOOST_PATH, "project-config.jam"), "a") as jam:
    jam.write("using mpi ;\n")
  subprocess.check_call(["./b2", "--with-mpi", "--with-serialization", "--with-graph"])

def build_bpp(package):
  os.chdir(os.path.join(const.BPP_PATH, "bpp-" + package))
  mkdirnocheck("build")
  os.chdir("build")
  subprocess.check_call(["cmake", "-DCMAKE_INSTALL_PREFIX=" + const.BPP_INSTALL_PATH, ".."])
  subprocess.check_call(["make"])
  subprocess.check_call(["make", "install"])

def build_pll():
  os.chdir(const.PLL_PATH)
  subprocess.check_call("autoconf")
  try:
    subprocess.check_call("./configure")
  except Exception:
    subprocess.check_call("autoreconf --install")
    subprocess.check_call("./configure")
    pass
  subprocess.check_call("make")

def copyFilesFromPattern(pattern, destDir):
  for f in glob.glob(pattern):
    shutil.copyfile(f, os.path.join(destDir, os.path.basename(f)))

def copy_deps():
  print("Warning, this may be dangerous if DEPS_PATH is not well set")
  # prepare directories
  rmnocheck(const.DEPS_PATH)
  os.mkdir(const.DEPS_PATH)
  os.mkdir(const.DEPS_LIB_PATH)
  os.mkdir(const.DEPS_INCLUDE_PATH)
  os.mkdir(const.DEPS_INCLUDE_PLLMODULES_PATH)
  os.mkdir(const.DEPS_INCLUDE_PLL_PATH)
  # bpp headers and libraries
  shutil.copytree(const.BPP_INSTALL_INCLUDE_PATH, const.DEPS_INCLUDE_BPP_PATH)
  copyFilesFromPattern( os.path.join(const.BPP_INSTALL_PATH, "lib64", "*.so*"), const.DEPS_LIB_PATH)
  # libpll2 headers and libraries
  copyFilesFromPattern(os.path.join(const.LIBPLL2_SRC_PATH, "*.h"), const.DEPS_INCLUDE_PLLMODULES_PATH)
  copyFilesFromPattern(os.path.join(const.LIBPLL2_SRC_PATH, ".libs", "*.so*" ), const.DEPS_LIB_PATH)
  # pllmodules headers and libraries
  copyFilesFromPattern(os.path.join(const.PLLMODULES_SRC_PATH, "*", "*.h"), const.DEPS_INCLUDE_PLLMODULES_PATH)
  copyFilesFromPattern(os.path.join(const.PLLMODULES_SRC_PATH, "*", ".libs", "*.so*" ), const.DEPS_LIB_PATH)
  # old pll headers and libraries
  copyFilesFromPattern(os.path.join(const.PLL_SRC_PATH, "*.h" ), const.DEPS_INCLUDE_PLL_PATH)
  copyFilesFromPattern(os.path.join(const.PLL_SRC_PATH, ".libs", "*.so*" ), const.DEPS_LIB_PATH)
  
def build_phyldog():
  os.chdir(const.PHYLDOG_PATH)
  mkdirnocheck("build")
  os.chdir(os.path.join(const.PHYLDOG_PATH, "build"))
  dcmakeLib = '-DCMAKE_LIBRARY_PATH=' + const.DEPS_LIB_PATH + "/" 
  dcmakeInclude = '-DCMAKE_INCLUDE_PATH=' + const.DEPS_INCLUDE_PATH + "/" 
  dboostLibrary = '-DBOOST_LIBRARYDIR=' + const.BOOST_LIB_PATH + "/"
  dboostRoot = '-DBOOST_ROOT=' + const.BOOST_PATH + "/"
  dcompiler = '-DCMAKE_CXX_STANDARD = 11'
  cmakeCommand = ['cmake', '..', dcmakeLib, dcmakeInclude, dboostLibrary, dboostRoot]
  subprocess.check_call(cmakeCommand)
  subprocess.check_call("make")


start_time = time.time()

build_raxml()
build_boost()
build_bpp("core")
build_bpp("seq")
build_bpp("phyl")
build_pll()
copy_deps()
build_phyldog()

elapsed = time.time() - start_time
print("END OF THE INSTALLATION. ELAPSED TIME: " + str(elapsed) + "seconds")

