import sys;
import os;


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

def buildRaxmlCommand(optionsFile):
    """ 
    Read a phyldog gene option file
    and build a raxml command
    """
    return []
    
def buildRaxmlCommands(optionsPath):
    """
    Call buildRaxmlCommand on each file in optionsPath
    and return a list of raxml commands to execute
    """
    commands = []
    for optionsFile in os.listdir(optionsPath):
        f = os.path.join(optionsPath, optionsFile)
        commands.append(buildRaxmlCommand(f))
    return commands

def runRaxmlCommands(commands, threadsNumber):
    """
    Run concurrently one raxml instance per command
    """
    print("TO IMPLEMENT")

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
    # copy all necessary files
    generalOptionsFile = duplicateOptionFiles(optionsPath, outputPath)
    # build raxml commands
    raxmlCommands = buildRaxmlCommands(optionsPath)
    # execute raxml commands
    runRaxmlCommands(raxmlCommands, threadsNumber)
    # execute phyldog
    runPhyldog(generalOptionsFile, threadsNumber)

