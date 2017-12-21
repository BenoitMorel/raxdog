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

    def initFromOptionFile(self, geneDict, outputTreesPath):
        """
        Load all parameters from an optionFile
        (optionFile is a string)
        todobenoit: outputTreesPath should be read from optionFile somehow
        """
        self.model = "GTR"
        self.msaFile = geneDict["input.sequence.file"]
        self._parseFastaDimensions(self.msaFile)
        print("Sites : " + str(self.sites))
        optim = (self.sites + 999) // 1000
        self.optimalThreadsNumber = 2 **(optim.bit_length() - 1)
        self.prefix = os.path.basename(self.msaFile)
        self.prefix = os.path.splitext(self.prefix)[0]
        self.prefix = os.path.join(outputTreesPath, self.prefix)

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
        print("Executing " + str(command))
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

