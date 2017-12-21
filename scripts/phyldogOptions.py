import re

def replaceLinesStartingWith(inputFile, start, newLine):
  with open(inputFile) as readFile:
    lines = readFile.readlines()
  with open(inputFile,'w') as w:
    for line in lines:
      if line.startswith(start):
        w.write(newLine + "\n")
      else:
        w.write(line)
  
def fixListGenes(inputFile, newOptionsDir):
  with  open(inputFile) as readFile:
    lines = readFile.readlines()
  with open(inputFile,'w') as w:
    for line in lines:
      f = line.split('/')[-1]
      w.write(os.path.join(newOptionsDir,f)) 


def get(optionFile, optionName, defaultValue):
    res = defaultValue
    with open(optionFile) as f:
        for line in f:
            if line.startswith(optionName):
                res = line.split("=")[1][:-1]
    print("get " + res)
    return res

def computeOptionsDico(optionFile):
    dico = {}
    lines = []
    with open(optionFile) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("#"):
            continue
        split = line.split("=")
        if (len(split) == 2):
            value = split[1][:-1]
            while True:
                match = re.search(r'\$\(([^\)]*)\)', value)
                if(match):
                    toReplace = "$(" + match.group(1) + ")"
                    value = value.replace(toReplace, dico[match.group(1)]) 
                else:
                    break
            dico[split[0]] = value
    return dico

dico = computeOptionsDico("/home/benoit/github/raxdog/data/DataExampleSmall/OptionFiles/HBG011000.opt")

for key in dico.keys():
    print(key + ":" + dico[key])


def preparePhydlogFiles(dataPath, outputPath, seed, speciesNumber, genesNumber, method, startingTrees):
  """ 
  Create a new directory, extract and modify an original dataset to this directory, and return the directory name
  prefix and suffix are appended at the begining and the end of the new directory name
  """

  if (startingTrees == "bionj"):
    useBestTrees = False
  elif (startingTrees == "raxmlStart"):
    useBestTrees = True
    geneTreeSuffix = ".raxml.startTree"
  elif (startingTrees == "raxmlParsi"):
    useBestTrees = True
    geneTreeSuffix = ".raxml.parsiTree"
  elif (startingTrees == "raxmlBest"):
    useBestTrees = True
    geneTreeSuffix = ".raxml.bestTree"
  else:
    raise Exception('Invalid startingTrees mode')
  # get paths
  path = os.path.dirname(os.path.realpath(__file__))
  phyldogDir = os.path.dirname(path)
  outputDir = prefix + "_" + dataset + "_" + seed + "_" + speciesNumber + "_" + genesNumber + "_" + method + "_" + startingTrees + suffix
  outputDir = os.path.join(path, outputDir)
  originDataDir = os.path.join(phyldogDir, "benoitdata", dataset)
  originOptionsDir = os.path.join(originDataDir, "OptionFiles")
  newDataDir = os.path.join(outputDir, dataset)
  newOptionsDir = os.path.join(newDataDir, "OptionFiles")
  newGeneralOptionsFile = os.path.join(newOptionsDir, "GeneralOptions.txt")
  geneTreesDir = os.path.join(originDataDir, "RaxmlTrees")
  resultsDir = os.path.join(outputDir, "results")
  # create directories
  shutil.rmtree(outputDir, True)
  os.mkdir(outputDir)
  os.mkdir(newDataDir)
  os.mkdir(resultsDir)
  # build the options files
  shutil.copytree(originOptionsDir, newOptionsDir)
  resizeFile(os.path.join(newOptionsDir, "listSpecies.txt"), int(speciesNumber))
  resizeFile(os.path.join(newOptionsDir, "listGenes.txt"), int(genesNumber))
  fixListGenes(os.path.join(newOptionsDir, "listGenes.txt"), newOptionsDir)
  replaceLinesStartingWith(newGeneralOptionsFile, "RESULT=", "RESULT=" + outputDir + "/") 
  replaceLinesStartingWith(newGeneralOptionsFile, "OPT=", "OPT=" + newOptionsDir + "/") 
  with open(newGeneralOptionsFile, "a") as w:
    w.write("rearrangement.gene.tree=spr\n")
    w.write("reset.gene.trees=no\n")
    w.write("likelihood.evaluator=" + method + "\n")
    w.write("seed=" + seed + "\n")
  # build per gene files
  if (useBestTrees):
    notFoundCount = 0
    optionsFilenames = (opt for opt in os.listdir(newOptionsDir) if opt.endswith(".opt"))
    for opt in optionsFilenames:
      geneName = os.path.splitext(opt)[0]
      optFile = os.path.join(newOptionsDir, opt)
      geneTreeFile = os.path.join(geneTreesDir, geneName + geneTreeSuffix)
      replaceLinesStartingWith(optFile, "RESULT=", "RESULT=" + resultsDir + "/")
      if os.path.isfile(geneTreeFile):
        replaceLinesStartingWith(optFile, "init.gene.tree=bionj", "init.gene.tree=user")
        replaceLinesStartingWith(optFile, "gene.tree.file=", "gene.tree.file=" + geneTreeFile)
      else:
        print("Warning: " + geneTreeFile + " not found")
        notFoundCount += 1
    if notFoundCount > 0:
      print("Failed to find " + str(notFoundCount) + " genes trees files. Bionj trees will be generated instead") 
  return outputDir

