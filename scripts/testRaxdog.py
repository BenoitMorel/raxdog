import raxdog
import os
import shutil

outputPath = "/home/morelbt/github/raxdog/results/dataexample/"
optionsFile = "/home/morelbt/github/raxdog/data/DataExample/OptionFiles/GeneralOptions.txt"
threadsNumber = 8
try: 
  shutil.rmtree(outputPath) 
except:
    pass
raxdog.raxdog(optionsFile, outputPath, threadsNumber)

