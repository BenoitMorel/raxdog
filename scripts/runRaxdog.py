import sys
import raxdog

def printHelp():
  print("Usage: python runRaxdog optionPath outputPath threadsNumber")


if (len(sys.argv) != 4):
  print("Wrong syntax") 
  printHelp()

optionsPath = sys.argv[1]
outputPath = sys.argv[2]
threadsNumber = int(sys.argv[3])

raxdog.raxdog(optionsPath, outputPath, threadsNumber)




