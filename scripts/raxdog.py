import sys
import os
import raxmlCommand
import raxmlCommandsRunner as raxmlRunner
import raxdogconstants as const; 
import phyldogRunner
import dirutils
import shutil
import phyldogOptions as opt
import fileinput

def buildRaxmlCommands(geneDicts, outputTreesPath, threadsNumber):
    """
    Parse all the gene options files in optionsPath
    and return a list of raxml commands to execute
    """
    commands = []
    for geneDict in geneDicts.values():
        if geneDict.get(const.PREPROC_TREE_MODE) == "raxml":
            command = raxmlCommand.RaxmlCommand()
            command.initFromOptionFile(geneDict, outputTreesPath, threadsNumber)
            commands.append(command)
    return commands

def runRaxmlCommands(commands, threadsNumber, svgOutput):
    """
    Run concurrently one raxml instance per command
    """
    r = raxmlRunner.RaxmlCommandsRunner(threadsNumber)
    for command in commands:
        r.addJob(command)
    r.run(svgOutput)

def replacePath(oldOptionsPath, newOptionsPath, fileName):
  with fileinput.FileInput(fileName, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(oldOptionsPath, newOptionsPath), end='')

def updateResultPath(outputPath, fileName):
  with fileinput.FileInput(fileName, inplace=True, backup='.bak') as file:
    for line in file:
      if (line.startswith("RESULT=")):
        print("RESULT=" + outputPath + "/")
      else:
        print(line, end='')

def replacePathInOptions(outputPath, oldOptionsPath, newOptionsPath):
    oldGeneralOptionsFile = os.path.join(oldOptionsPath, "GeneralOptions.txt")
    newGeneralOptionsFile = os.path.join(newOptionsPath, "GeneralOptions.txt")
    
    newOptions = opt.PhyldogOptions(newGeneralOptionsFile)
    newGeneralDict = newOptions.getGeneralDict()
    genelistFile = newGeneralDict.get("genelist.file")
    # update general options file
    replacePath(oldOptionsPath, newOptionsPath, newGeneralOptionsFile)
    replacePath(oldOptionsPath, newOptionsPath, genelistFile)
    updateResultPath(outputPath, newGeneralOptionsFile)
    # update genes options files
    with open(genelistFile) as f:
      for line in f.readlines():
        geneOptionFile = line.split(":")[0]
        updateResultPath(outputPath, geneOptionFile)


def raxdog(optionsPath, outputPath, threadsNumber):
    """
    Whole raxdog pipeline
    """
    try:
      os.makedirs(outputPath)
    except:
      pass

    # duplicate options files and update paths
    print("Duplicating option paths...")
    newOptionsPath = os.path.join(outputPath, "OptionFiles")
    shutil.copytree(optionsPath, newOptionsPath)
    replacePathInOptions(outputPath, optionsPath, newOptionsPath) 


    # create directoies
    print("Creating directories...")
    generalOptionsFile = os.path.join(newOptionsPath, "GeneralOptions.txt")
    outputTreesPath = os.path.join(outputPath, "RaxmlTrees")
    os.makedirs(outputTreesPath)
    options = opt.PhyldogOptions(generalOptionsFile)
    phyldogOutputPath = os.path.join(outputPath, "phyldogOutputs")
    os.makedirs(phyldogOutputPath)
    svgOutput = os.path.join(outputPath, "multi-raxml.svg")

    # build raxml commands
    print("Building raxml commands...")
    raxmlCommands = buildRaxmlCommands(options.getGeneDicts(), outputTreesPath, threadsNumber)
    
    print("Running raxml commands...")
    # execute raxml commands
    runRaxmlCommands(raxmlCommands, threadsNumber, svgOutput)
    
    # execute phyldog
    # print("Running phyldog...")
    #os.chdir(phyldogOutputPath)
    
    #phyldogRunner.runPhyldog(generalOptionsFile, threadsNumber)


