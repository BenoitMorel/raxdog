import os

RAXDOG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
THIRDLIB_PATH= os.path.join(RAXDOG_ROOT, "thirdlib")
RAXML_PATH= os.path.join(THIRDLIB_PATH, "raxml-ng")
PHYLDOG_PATH= os.path.join(THIRDLIB_PATH, "PHYLDOG")
PLLMODULES_PATH= os.path.join(RAXML_PATH, "libs", "pll-modules")
LIBPLL2_PATH= os.path.join(PLLMODULES_PATH, "libs", "libpll")
BOOST_PATH= os.path.join(THIRDLIB_PATH, "boost")
BOOST_LIB_PATH= os.path.join(BOOST_PATH, "stage", "lib")
BPP_PATH= os.path.join(THIRDLIB_PATH, "bpp")
PLL_PATH= os.path.join(THIRDLIB_PATH, "phylogenetic-likelihood-library")

BPP_INSTALL_PATH = os.path.join(BPP_PATH, "bppinstall")

BPP_INSTALL_INCLUDE_PATH = os.path.join(BPP_INSTALL_PATH, "include", "Bpp")
PLLMODULES_SRC_PATH = os.path.join(PLLMODULES_PATH, "src")
LIBPLL2_SRC_PATH = os.path.join(LIBPLL2_PATH, "src")
PLL_SRC_PATH = os.path.join(PLL_PATH, "src")

DEPS_PATH = os.path.join(THIRDLIB_PATH, "deps")
DEPS_LIB_PATH = os.path.join(DEPS_PATH, "lib")
DEPS_INCLUDE_PATH = os.path.join(DEPS_PATH, "include")
DEPS_INCLUDE_BPP_PATH = os.path.join(DEPS_INCLUDE_PATH, "Bpp")
DEPS_INCLUDE_PLLMODULES_PATH = os.path.join(DEPS_INCLUDE_PATH, "pllmodules")
DEPS_INCLUDE_PLL_PATH = os.path.join(DEPS_INCLUDE_PATH, "pll")


