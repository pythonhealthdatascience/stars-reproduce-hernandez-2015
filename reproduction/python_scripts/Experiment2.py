# Experiment 2 (Figure 7)
# Bi-objective model + alter percentage of pre-screened (10%, 20%, 30%... 90%)

# Run time: TODO add runtime
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os import listdir
from os.path import isfile, join
from main import run_experiment

# Path to scenarios
mypath = r'../inputs'

# Name of experiment files identified from path to scenarios
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Path to save results
experimentFolder = '../python_outputs/experiment2'

# Run experiment
run_experiment(mypath=mypath,
               experimentFolder=experimentFolder,
               experimentFiles=experimentFiles,
               runs=1,
               population=50,
               generations=25,
               # Minimise staff number, maximise throughput
               objectiveTypes=[False, True])
