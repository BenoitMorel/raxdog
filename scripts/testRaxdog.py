import raxdog
import os
import shutil

outputPath = "/home/benoit/github/raxdog/results/test1/"
optionsPath = "/home/benoit/github/raxdog/data/DataExample_10G/OptionFiles"
threadsNumber = 4
shutil.rmtree(outputPath) 
raxdog.raxdog(optionsPath, outputPath, threadsNumber)

