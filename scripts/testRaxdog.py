import raxdog
import os
import shutil

outputPath = "/home/benoit/github/raxdog/results/testsmall/"
optionsFile = "/home/benoit/github/raxdog/data/DataExampleSmall/OptionFiles/GeneralOptions.txt"
threadsNumber = 4
try: 
  shutil.rmtree(outputPath) 
except:
    pass
raxdog.raxdog(optionsFile, outputPath, threadsNumber)

