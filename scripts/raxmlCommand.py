import raxdogconstants as const; 
import os;
import subprocess;
import phyldogOptions as opt
import time

def commandKey(command):
    print("WARNING : dangerous magic number here (todobenoit)")
    return command.getThreads() * 10000000 + command.getExecutionTime() 

class RaxmlCommand:
    def __init__(self):
        # command 
        self.msaFile = "" # path to the msa
        self.model = ""   # substitution model
        self.prefix = ""  
        self.sites = 0
        self.optimalThreadsNumber = 1
        self.gene = ""
        # running 
        self.startTime = 0
        self.endTime = 0
        self.threadIndex = 0

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
        self.gene = geneDict["DATA"]
        #print("Sites : " + str(self.sites))
        optim = (self.sites + 999) // 1000
        self.optimalThreadsNumber = min(maxThreads, 2 **(optim.bit_length() - 1))
        tree = geneDict.get("gene.tree.file")
        print("TREE " + tree)
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
        self.startTime = time.time()
        command = []
        # todobenoit: do not hardcode per node cores number  
        nodesNumber = (self.optimalThreadsNumber - 1) // 8 + 1
        threadsNumber = min(self.optimalThreadsNumber, 8)
        if (nodesNumber > 1):
          command.append("mpirun")
          command.append("-np")
          command.append(str(nodesNumber))
        command.append(const.RAXML_EXEC)
        command.append("--msa")
        command.append(self.msaFile)
        command.append("--model")
        command.append(self.model)
        command.append("--threads")
        command.append(str(threadsNumber))
        command.append("--prefix")
        command.append(self.prefix)
        command.append("--site-repeats")
        command.append("on")
        for param in command:
          print(param, end=' ')
        print("")
        print("Executing " + str(command) + "\n")
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(command)
        self.endTime = time.time()

    def getThreads(self):
        return self.optimalThreadsNumber

    def getExecutionTime(self):
        return self.sites * self.nodes

class DebugCommand:
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

