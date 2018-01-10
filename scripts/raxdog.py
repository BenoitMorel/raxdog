import sys
import os
import raxmlCommand
import raxmlCommandsRunner as raxmlRunner
import raxdogconstants as const; 
import phyldogRunner
import dirutils
import shutil
import phyldogOptions as opt

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

def raxdog(generalOptionsFile, outputPath, threadsNumber):
    """
    Whole raxdog pipeline
    """
    os.makedirs(outputPath)
    outputTreesPath = os.path.join(outputPath, "RaxmlTrees")
    os.makedirs(outputTreesPath)
    options = opt.PhyldogOptions(generalOptionsFile)
    phyldogOutputPath = os.path.join(outputPath, "phyldogOutputs")
    os.makedirs(phyldogOutputPath)
    svgOutput = os.path.join(outputPath, "multi-raxml.svg")
    # build raxml commands
    raxmlCommands = buildRaxmlCommands(options.getGeneDicts(), outputTreesPath, threadsNumber)
    # execute raxml commands
    runRaxmlCommands(raxmlCommands, threadsNumber, svgOutput)
    # execute phyldog
    #os.chdir(phyldogOutputPath)
    #phyldogRunner.runPhyldog(generalOptionsFile, threadsNumber)


