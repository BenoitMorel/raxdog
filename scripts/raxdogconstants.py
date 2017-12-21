import os;

RAXDOG_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# directories
THIRDLIB_PATH = os.path.join(RAXDOG_ROOT, "thirdlib")
RAXML_PATH = os.path.join(THIRDLIB_PATH, "raxml-ng")
PHYLDOG_PATH = os.path.join(THIRDLIB_PATH, "PHYLDOG")
RAXML_BUILD_PATH = os.path.join(RAXML_PATH, "build")

# executables
RAXML_EXEC = os.path.join(RAXML_PATH, "bin", "raxml-ng-mpi")
PHYLDOG_EXEC = os.path.join(PHYLDOG_PATH, "build", "bin", "phyldog")

#option
PREPROC_TREE_MODE = "preprocessing.mode"
