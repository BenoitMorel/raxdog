import raxdog
import os
import shutil

outputPath = "/home/morelbt/github/raxdog/results/dataexample_plop/"
optionsPath = "/home/morelbt/github/raxdog/data/DataExample/OptionFiles/"
threadsNumber = 4





try: 
  shutil.rmtree(outputPath) 
except:
    pass
raxdog.raxdog(optionsPath, outputPath, threadsNumber)

