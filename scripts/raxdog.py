import sys
import os
import raxmlCommand
import raxmlCommandsRunner as raxmlRunner
import raxdogconstants as const; 
import phyldogRunner
import dirutils
import shutil
import phyldogOptions as opt

def buildRaxmlCommands(optionsPath, outputTreesPath):
    """
    Parse all the gene options files in optionsPath
    and return a list of raxml commands to execute
    """
    commands = []
    for optionsFile in os.listdir(optionsPath):
        if optionsFile.endswith(".opt"):
            f = os.path.join(optionsPath, optionsFile)

            if opt.get(f, const.PREPROC_TREE_MODE, "") == "raxml":
                command = raxmlCommand.RaxmlCommand()
                command.initFromOptionFile(f, outputTreesPath)
                commands.append(command)
    return commands

def runRaxmlCommands(commands, threadsNumber):
    """
    Run concurrently one raxml instance per command
    """
    r = raxmlRunner.RaxmlCommandsRunner(threadsNumber)
    for command in commands:
        r.addJob(command)
        print("r.addJob " + str(command.getThreads()))
        #command.execute(threadsNumber)
    r.run()

def raxdog(generalOptionsFile, outputPath, threadsNumber):
    """
    Whole raxdog pipeline
    """
    os.makedirs(outputPath)
    outputTreesPath = os.path.join(outputPath, "RaxmlTrees")
    os.makedirs(outputTreesPath)
    dico = opt.computeOptionsDico(generalOptionsFile)
    phyldogOutputPath = os.path.join(outputPath, "phyldogOutputs")
    optionsPath = dico["OPT"]
    os.makedirs(phyldogOutputPath)
    # build raxml commands
    raxmlCommands = buildRaxmlCommands(optionsPath, outputTreesPath)
    # execute raxml commands
    runRaxmlCommands(raxmlCommands, threadsNumber)
    # execute phyldog
    os.chdir(phyldogOutputPath)
    #phyldogRunner.runPhyldog(generalOptionsFile, threadsNumber)


