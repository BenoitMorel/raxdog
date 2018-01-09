import os
import sys

def activateRaxmlPreprocess(optionsPath):
  for optionFile in os.listdir(optionsPath):
    if not optionFile.endswith("opt"):
      print("continue")
      continue
    with open(os.path.join(optionsPath, optionFile), "a") as f:
      print("write")
      f.write("\ninit.gene.tree=user")
      f.write("\ngene.tree.file=$(RESULT)$(DATA).raxml.bestTree")
      f.write("\npreprocessing.mode=raxml\n")

print(sys.argv[1])
activateRaxmlPreprocess(sys.argv[1])

