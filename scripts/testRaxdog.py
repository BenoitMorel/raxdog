import raxdog
import os
import shutil

outputPath = "/home/benoit/github/raxdog/results/testsmall/"
optionsPath = "/home/benoit/github/raxdog/data/DataExampleSmall/OptionFiles"
threadsNumber = 4
#shutil.rmtree(outputPath) 
raxdog.raxdog(optionsPath, outputPath, threadsNumber)

