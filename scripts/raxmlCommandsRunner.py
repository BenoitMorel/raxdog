#!/usr/bin/python3.5
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import raxmlCommand
import svgwriter

class Notifier:
    _raxmlCommandsRunner = 0
    _job = 0
    def __init__(self, raxmlCommandsRunner, job):
        self._raxmlCommandsRunner = raxmlCommandsRunner
        self._job = job

    def notify(self, future):
        self._raxmlCommandsRunner.jobEnded(self._job)


class RaxmlCommandsRunner:
    def __init__(self,totalAvailableThreads):
        self._totalAvailableThreads = totalAvailableThreads
        self._executor = ThreadPoolExecutor(totalAvailableThreads)
        self._jobs = []
        self._nextJobIndex = 0
        self._futures = []
        self._remainingThreads = totalAvailableThreads
        self._nextJobIndex = 0
        self._svgWriter = None
        self._startTime = 0

    def jobEnded(self, job):
        print("job ended " + str(job.threadIndex) + " "  + str(job.getThreads()))
        self._remainingThreads += job.getThreads()
        self._svgWriter.drawRec(100 * job.threadIndex, job.startTime - self._startTime, 100 * job.getThreads(), job.endTime - job.startTime, job.gene)
        print("Free " + str(job.getThreads()) + " threads. Remaining: " + str(self._remainingThreads))
        self.runAllPossibleJobs(job.threadIndex)

    def addJob(self, job):
        self._jobs.append(job)
        
    def hasNextJob(self):
        return self._nextJobIndex < len(self._jobs)

    def getNextJob(self):
        return self._jobs[self._nextJobIndex]
    
    def popJob(self):
        self._nextJobIndex += 1

    def canRunNextJob(self):
        return self.hasNextJob() and self.getNextJob().getThreads() <= self._remainingThreads
        
    def runJob(self, job, threadIndex):
        print("Allocate " + str(job.getThreads()) + " threads")
        self._remainingThreads -= job.getThreads()
        job.threadIndex = threadIndex
        f = self._executor.submit(job.execute)
        notifier = Notifier(self, job)
        f.add_done_callback(notifier.notify)
        self._futures.append(f)
        self.popJob()

    def runAllPossibleJobs(self, threadIndex):
        while (self.canRunNextJob()):
          job = self.getNextJob()
          self.runJob(job, threadIndex)
          threadIndex += job.optimalThreadsNumber



    def run(self, svgOutput):
        print("Starting multi raxml...")
        self._startTime = time.time()
        self._svgWriter = svgwriter.SVGWriter(svgOutput)
        begin = time.time()
        self._jobs.sort(key=raxmlCommand.commandKey, reverse=True)
        self.runAllPossibleJobs(0)
        while(not self.allJobsEnded()):
            time.sleep(0.05)
        end = time.time()
        self._svgWriter.close()
        print("End of multi raxml (" + str(end - begin) + "s)") 

    def allJobsEnded(self):
        if (self.hasNextJob()):
            return False
        for f in self._futures:
            if f.running():
                return False
        return True

