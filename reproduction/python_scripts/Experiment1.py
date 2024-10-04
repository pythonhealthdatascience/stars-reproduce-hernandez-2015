# Experiment 1
# Run with a population of 100 and 50 generations
# Alter percentage of pre-screened (10%, 20%, 30%,... 90%)
# Used to produce Figure 5 and 6

from os import listdir
from os.path import isfile, join
from main import run_experiment

# Path to scenarios
mypath = r'../inputs'

# Name of experiment files identified from path to scenarios
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Path to save results
experimentFolder = '../python_outputs/experiment1'

# Run expertiment
run_experiment(mypath=mypath,
               experimentFolder=experimentFolder,
               experimentFiles=experimentFiles,
               runs=1,
               population=1,
               generations=1)
