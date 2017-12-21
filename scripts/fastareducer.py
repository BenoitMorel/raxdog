import os


def reduceFile(fastaFile):
    toWrite = []
    with open(fastaFile) as f:
        lines = f.readlines()
        printNext = False
        for line in lines:
            if (printNext):
                toWrite.append(line)
                printNext = False
                continue
            if (line.startswith(">")):
                toWrite.append(line)
                printNext = True
    with open(fastaFile, "w") as f:
        for line in toWrite:
            f.write(line)

def reduceFilesIn(fastaDir):
    for f in os.listdir(fastaDir):
        reduceFile(os.path.join(fastaDir, f))

reduceFilesIn("/home/benoit/github/raxdog/data/DataExampleSmall/testFastaFiles/")
        
