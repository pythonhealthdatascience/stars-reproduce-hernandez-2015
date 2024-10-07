# Experiment 3 (Figure 8)
# Tri-objective model + (a) 100 pop 50 gen (b) 200 pop 100 gen (c) 50 pop 25 gen

# Run time: TODO add runtime
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os import listdir
from os.path import isfile, join
import datetime
from multiprocessing import Pool
from main import wrapper

# Set to default
mypath = r'../inputs'
file = '10-prescreened.txt'
runs = 1
objectiveTypes = [False, True, False]

# Path to save results
experimentFolder = '../python_outputs/experiment3'

# Scenarios to run for this experiment
scenarios = [
    {
        'population': 100,
        'generations': 50,
        'solutionpath': join(experimentFolder, '100pop50gen')
    },
    {
        'population': 200,
        'generations': 100,
        'solutionpath': join(experimentFolder, '200pop100gen')
    },
    {
        'population': 50,
        'generations': 25,
        'solutionpath': join(experimentFolder, '50pop25gen')
    }
]

# Start timer
startTime = datetime.datetime.now()

# Create parameter list for each experiment
params = [
    {'mypath': mypath,
     'experimentFolder': experimentFolder,
     'file': file,
     'runs': runs,
     'population': scenario['population'],
     'generations': scenario['generations'],
     'objectiveTypes': objectiveTypes,
     'solutionpath': scenario['solutionpath']}
    for scenario in scenarios
]

# Create a process pool that uses all CPUs
pool = Pool()
try:
    # Map the run_scenario function to the experiment files
    results = pool.map(wrapper, params)
finally:
    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()

# End timer and save time for that result
endTime = datetime.datetime.now()
with open(join(experimentFolder, "time.txt"), "w") as text_file:
    text_file.write("{0}".format(endTime - startTime))
