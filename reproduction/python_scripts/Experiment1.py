# Experiment 1 (Figure 5 and 6 and Appendix A.2)
# Tri-objective model + alter percentage of pre-screened (10%, 20%, 30%... 90%)

# Run time: 4 hours 28 minutes
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os import listdir
from os.path import isfile, join
from main import run_experiment

# Path to scenarios
mypath = r'../inputs'

# Name of experiment files identified from path to scenarios
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Path to save results
experimentFolder = '../python_outputs/experiment1'

# Run experiment
run_experiment(mypath=mypath,
               experimentFolder=experimentFolder,
               experimentFiles=experimentFiles,
               # Amendment from paper: 1 run instead of 3
               runs=1,
               population=100,
               generations=50,
               # Minimise staff number, maximise throughput, minimise wait time
               objectiveTypes=[False, True, False])
