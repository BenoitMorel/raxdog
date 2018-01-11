import re
import os

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
    return res

def parseDico(optionFile):
    dico = {}
    lines = []
    with open(optionFile) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("#"):
            continue
        split = line.split("=")
        if (len(split) != 2):
            continue
        value = split[1][:-1]
        pattern = r'\$\(([^\)]*)\)'
        match = re.search(pattern, value)
        while match:
            toReplace = "$(" + match.group(1) + ")"
            value = value.replace(toReplace, dico[match.group(1)]) 
            match = re.search(pattern, value)
        dico[split[0]] = value
    return dico


class PhyldogOptions:
    
    def __init__(self, generalOptionsFile):
        self.dicts = {} # dict of dict. 
        self.generalDict = {} # dict
        print("INIT OPTIONS " + generalOptionsFile)
        print(len(self.dicts))
        self.generalDict = parseDico(generalOptionsFile)
        genelistFile = self.generalDict.get("genelist.file")
        print(  "gene list " + genelistFile)
        with open(genelistFile) as f:
          for line in f.readlines():
            geneOptionFile = line.split(":")[0]
            self.dicts[geneOptionFile] = parseDico(geneOptionFile)
        print(len(self.dicts))

    def getGeneralDict(self):
        return self.generalDict

    def getGeneDict(self, optionsFile):
        return self.dicts[optionsFile]

    def getGeneDicts(self):
        return self.dicts

