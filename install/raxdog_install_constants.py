import os

RAXDOG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
RAXML_PATH= os.path.join(RAXDOG_ROOT, "raxml-ng")
BOOST_PATH= os.path.join(RAXDOG_ROOT, "boost")
BPP_PATH= os.path.join(RAXDOG_ROOT, "bpp")
BPP_INSTALL_PATH = os.path.join(BPP_PATH, "bppinstall")



