import os

RAXDOG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
RAXML_PATH= os.path.join(RAXDOG_ROOT, "raxml-ng")
PLLMODULES_PATH= os.path.join(RAXML_PATH, "libs", "pll-modules")
LIBPLL2_PATH= os.path.join(PLLMODULES_PATH, "libs", "libpll")
BOOST_PATH= os.path.join(RAXDOG_ROOT, "boost")
BPP_PATH= os.path.join(RAXDOG_ROOT, "bpp")
PLL_PATH= os.path.join(RAXDOG_ROOT, "phylogenetic-likelihood-library")

BPP_INSTALL_PATH = os.path.join(BPP_PATH, "bppinstall")

BPP_INSTALL_INCLUDE_PATH = os.path.join(BPP_INSTALL_PATH, "include", "Bpp")
PLLMODULES_SRC_PATH = os.path.join(PLLMODULES_PATH, "src")
LIBPLL2_SRC_PATH = os.path.join(LIBPLL2_PATH, "src")
PLL_SRC_PATH = os.path.join(PLL_PATH, "src")

DEPS_PATH = os.path.join(RAXDOG_ROOT, "deps")
DEPS_LIB_PATH = os.path.join(DEPS_PATH, "lib")
DEPS_INCLUDE_PATH = os.path.join(DEPS_PATH, "include")
DEPS_INCLUDE_BPP_PATH = os.path.join(DEPS_INCLUDE_PATH, "Bpp")
DEPS_INCLUDE_PLLMODULES_PATH = os.path.join(DEPS_INCLUDE_PATH, "pllmodules")
DEPS_INCLUDE_PLL_PATH = os.path.join(DEPS_INCLUDE_PATH, "pll")


