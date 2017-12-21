import subprocess
import raxdogconstants as const


def runPhyldog(generalOptionsFile, threadsNumber):
    """
    Run phyldog on generalOptionsFile with threadsNumber
    threads
    """
    command = []
    command.append("mpirun")
    command.append("-np")
    command.append(str(threadsNumber))
    command.append(const.PHYLDOG_EXEC)
    command.append("param=" + generalOptionsFile)
    subprocess.check_call(command)



