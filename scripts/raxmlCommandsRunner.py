#!/usr/bin/python3.5
from concurrent.futures import ThreadPoolExecutor
import time
import sys


class Notifier:
    _raxmlCommandsRunner = 0
    _job = 0
    def __init__(self, raxmlCommandsRunner, job):
        self._raxmlCommandsRunner = raxmlCommandsRunner
        self._job = job

    def notify(self, future):
        self._raxmlCommandsRunner.jobEnded(self._job)

class Job:
    _threads = 1
    _executionTime = 0

    def __init__(self, executionTime, threads):
        self._threads = threads
        self._executionTime = executionTime

    def getThreads(self):
        return self._threads

    def getExecutionTime(self):
        return self._executionTime

    def execute(self):
        executor = ThreadPoolExecutor(self._threads)
        for i in range(0, self._threads):
            executor.submit(time.sleep, self._executionTime / self._threads)
        executor.shutdown()

class RaxmlCommandsRunner:
    _totalAvailableThreads = 1
    _executor = 1 
    _jobs = []
    _nextJobIndex = 0
    _remainingThreads = 0
    _futures = []
    def __init__(self,totalAvailableThreads):
        self._totalAvailableThreads = totalAvailableThreads
        self._executor = ThreadPoolExecutor()
        self._remainingThreads = totalAvailableThreads
        self._nextJobIndex = 0

    def jobEnded(self, job):
        self._remainingThreads += job.getThreads()
        print("Free " + str(job.getThreads()) + " threads. Remaining: " + str(self._remainingThreads))
        self.runAllPossibleJobs()

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
        
    def runJob(self, job):
        print("Allocate " + str(job.getThreads()) + " threads")
        self._remainingThreads -= job.getThreads()
        f = self._executor.submit(job.execute)
        notifier = Notifier(self, job)
        f.add_done_callback(notifier.notify)
        self._futures.append(f)
        self.popJob()

    def runAllPossibleJobs(self):
        while (self.canRunNextJob()):
            self.runJob(self.getNextJob())


    def run(self):
        self.runAllPossibleJobs()

    def allJobsEnded(self):
        if (self.hasNextJob()):
            return False
        for f in self._futures:
            if f.running():
                return False
        return True

runner = RaxmlCommandsRunner(4)
runner.addJob(Job(8, 4)) # 2 sec on 4 threads
runner.addJob(Job(8, 2)) # 4 sec on 2 threads
runner.addJob(Job(16, 2)) # 8 sec on 2 threads
runner.run() #should last 10 sec
while(not runner.allJobsEnded()):
    time.sleep(0.05)

