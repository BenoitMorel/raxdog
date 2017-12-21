import sys
import os
import raxmlCommand
import raxmlCommandsRunner as raxmlRunner
import phyldogRunner
import dirutils
import shutil

def buildRaxmlCommands(optionsPath, outputTreesPath):
    """
    Parse all the gene options files in optionsPath
    and return a list of raxml commands to execute
    """
    commands = []
    for optionsFile in os.listdir(optionsPath):
        if optionsFile.endswith(".opt"):
            f = os.path.join(optionsPath, optionsFile)
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

def raxdog(optionsPath, outputPath, threadsNumber):
    """
    Whole raxdog pipeline
    """
    dirutils.makedirsnocheck(outputPath)
    outputTreesPath = os.path.join(outputPath, "RaxmlTrees")
    dirutils.mkdirnocheck(outputTreesPath)
    # build raxml commands
    raxmlCommands = buildRaxmlCommands(optionsPath, outputTreesPath)
    # execute raxml commands
    print("HEY " + raxmlCommands[0].msaFile)
    runRaxmlCommands(raxmlCommands, threadsNumber)
    # execute phyldog
    phyldogRunner.runPhyldog(generalOptionsFile, threadsNumber)


