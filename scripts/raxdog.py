import sys
import os
import raxmlCommand
import raxmlCommandsRunner as runner

def duplicateOptionFiles(optionsPath, duplicateOptionsPath):
    """
    Copy the option files that need to be edited
    Update the paths accordingly.
    The GeneralOptions.txt and other directories
    are created in duplicateOptionsPath
    Returns the full path to the new GeneralOptions.txt
    """
    print("TO IMPLEMENT")
    return "notimplemented"

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
    r = runner.RaxmlCommandsRunner(threadsNumber)
    for command in commands:
        r.addJob(command)
        print("r.addJob " + str(command.getThreads()))
        #command.execute(threadsNumber)
    r.run()

def runPhyldog(generalOptionsFile, threadsNumber):
    """
    Run phyldog on generalOptionsFile with threadsNumber
    threads
    """
    print("TO IMPLEMENT")


def raxdog(optionsPath, outputPath, threadsNumber):
    """
    Whole raxdog pipeline
    """
    os.makedirs(outputPath)
    outputTreesPath = os.path.join(outputPath, "RaxmlTrees")
    os.mkdir(outputTreesPath)
    # copy all necessary files
    generalOptionsFile = duplicateOptionFiles(optionsPath, outputPath)
    # build raxml commands
    raxmlCommands = buildRaxmlCommands(optionsPath, outputTreesPath)
    # execute raxml commands
    print("HEY " + raxmlCommands[0].msaFile)
    runRaxmlCommands(raxmlCommands, threadsNumber)
    # execute phyldog
    runPhyldog(generalOptionsFile, threadsNumber)


