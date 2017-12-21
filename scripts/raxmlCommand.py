import raxdogconstants as const; 
import os;
import subprocess;

def commandKey(command):
    # todobenoit 10,000,000 does not work anymore with too many sites
    return command.getThreads() * 10000000 + command.getExecutionTime() 

def containsRaxml(optionFile):
    result = False
    with open(optionFile) as f:
        for line in f:
            if line.startswith(const.PREPROC_TREE_MODE):
                print(line.split("=")[1])
                if line.split("=")[1][:-1] == const.RAXML_PREPROC_TREE_MODE:
                    print("Raxml mode !!")
                    result = True
                else:
                    print("NO RAXML MODE")
                    result = False
    return result

class RaxmlCommand:
    msaFile = "" # path to the msa
    model = ""   # substitution model
    prefix = ""  
    sites = 0
    optimalThreadsNumber = 1

    def _parseNumberOfSites(self, fastaFile):
        sites = 0
        with open(fastaFile) as f:
            for line in f:
                if line.startswith(">") and sites != 0:
                    return sites
                sites += (len(line.replace(" ", "")) - 1)
        return 0

    def initFromOptionFile(self, optionFile, outputTreesPath):
        """
        Load all parameters from an optionFile
        (optionFile is a string)
        todobenoit: outputTreesPath should be read from optionFile somehow
        """
        self.model = "GTR"
        print("init from option file " + optionFile)
        with open(optionFile) as f:
            for line in f.readlines():
                if line.startswith("input.sequence"):
                    self.msaFile = line.split("=")[1][:-1]
                    break
        self.sites = self._parseNumberOfSites(self.msaFile)
        opt = (self.sites + 999) // 1000
        self.optimalThreadsNumber = 2 **(opt.bit_length() - 1)
        print("sites : " + str(self.sites))
        print("opt : " + str(self.optimalThreadsNumber))
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
        return self.sites

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

