import raxdogconstants as const; 
import os;
import subprocess;
import phyldogOptions as opt

def commandKey(command):
    print("WARNING : dangerous magic number here (todobenoit)")
    return command.getThreads() * 10000000 + command.getExecutionTime() 

class RaxmlCommand:
    msaFile = "" # path to the msa
    model = ""   # substitution model
    prefix = ""  
    sites = 0
    optimalThreadsNumber = 1

    def _parseFastaDimensions(self, fastaFile):
        self.sites = 0
        self.nodes = 0
        with open(fastaFile) as f:
            for line in f:
                if line.startswith(">"):
                    self.nodes += 1
                else:
                    self.sites += (len(line.replace(" ", "")) - 1)
        self.sites //= self.nodes

    def initFromOptionFile(self, geneDict, outputTreesPath, maxThreads):
        """
        Load all parameters from an optionFile
        (optionFile is a string)
        todobenoit: outputTreesPath should be read from optionFile somehow
        """
        self.model = "GTR"
        self.msaFile = geneDict["input.sequence.file"]
        self._parseFastaDimensions(self.msaFile)
        #print("Sites : " + str(self.sites))
        optim = (self.sites + 999) // 1000
        self.optimalThreadsNumber = min(maxThreads, 2 **(optim.bit_length() - 1))
        tree = geneDict.get("gene.tree.file")
        raxmlSuffix = ".raxml.bestTree"
        if tree == None or not tree.endswith(raxmlSuffix):
            raise Exception("Invalid gene.tree.file value : " + tree)
        if geneDict.get("init.gene.tree") != "user":
            raise Exception("Error: phyldog will ignore raxml tree because init.gene.tree is not set to user")
        self.prefix = tree[:-len(raxmlSuffix)]
        #print("prefix: " + self.prefix)
        

    def execute(self):
        """
        Run a raxml command on the current instance
        """
        command = []
        command.append(const.RAXML_EXEC)
        command.append("--msa")
        command.append(self.msaFile)
        command.append("--model")
        command.append(self.model)
        command.append("--threads")
        command.append(str(self.optimalThreadsNumber))
        command.append("--prefix")
        command.append(self.prefix)
        #print("Executing " + str(command))
        subprocess.check_call(command)

    def getThreads(self):
        return self.optimalThreadsNumber

    def getExecutionTime(self):
        return self.sites * self.nodes

class DebugCommand:
    _threads = 1
    _executionTime = 0

    def __init__(self, executionTime, threads):
        self._threads = threads
        self._executionTime = executionTime

    def getThreads(self):
        return self._threads

    def getExecutionTime(self):
        return self._executionTime

    def execute(self, threadsNumber):
        executor = ThreadPoolExecutor(threadsNumber)
        for i in range(0, self._threads):
            executor.submit(time.sleep, self._executionTime / threadsNumber)
        executor.shutdown()

