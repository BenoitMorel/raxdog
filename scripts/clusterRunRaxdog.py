import sys
import os
import subprocess
import shutil

def writeAndLaunchSubmit(optionPath, outputPath, threadsNumber):
  try: 
    shutil.rmtree(outputPath) 
  except:
    pass
  os.makedirs(outputPath)
  submitFile = os.path.join(outputPath, "submit.sh")
  runRaxdogScript = os.path.join(os.path.dirname(os.path.realpath(__file__)), "runRaxdog.py")
  with open(submitFile, "w") as f:
    print("todobenoit: handle number of threads")
    f.write("#!/bin/bash\n")
    f.write("#SBATCH -o " + os.path.join(outputPath, "myjob.out" ) + "\n")
    f.write("#SBATCH -N 1\n")
    f.write("#SBATCH -n 16\n")
    f.write("#SBATCH -B 2:8:1\n")
    f.write("#SBATCH --threads-per-core=1\n")
    f.write("#SBATCH --cpus-per-task=1\n")
    f.write("#SBATCH -t 24:00:00\n")
    f.write("\n")
    f.write("python " + runRaxdogScript + " " + optionPath + " " + outputPath + " " + str(threadsNumber) + "\n")
  subprocess.check_call(["sbatch", "-s", submitFile])



