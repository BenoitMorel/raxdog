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
  nodes = str((int(threadsNumber) - 1)//16 + 1)
  with open(submitFile, "w") as f:
    f.write("#!/bin/bash\n")
    f.write("#SBATCH -o " + os.path.join(outputPath, "myjob.out" ) + "\n")
    #f.write("#SBATCH -N " + str(nodes) + "\n")
    #f.write("#SBATCH -n " + str(threadsNumber) + "\n")
    f.write("#SBATCH -B 2:8:1\n")
    f.write("#SBATCH --ntasks-per-node=2\n")
    f.write("#SBATCH --ntasks-per-socket=1\n")
    f.write("#SBATCH --cpus-per-task=8 \n")
    f.write("#SBATCH --hint=compute_bound\n")
    f.write("#SBATCH -t 24:00:00\n")
    
    f.write("\n")
    f.write("python " + runRaxdogScript + " " + optionPath + " " + outputPath + " " + str(threadsNumber) + "\n")
  subprocess.check_call(["sbatch", "-s", "-N" + str(nodes) ,submitFile])



