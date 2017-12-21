import raxdog
import os
import shutil

outputPath = "/home/benoit/github/raxdog/results/testsmall/"
optionsPath = "/home/benoit/github/raxdog/data/DataExampleSmall/OptionFiles"
threadsNumber = 4
try: 
  shutil.rmtree(outputPath) 
except:
    pass
raxdog.raxdog(optionsPath, outputPath, threadsNumber)

