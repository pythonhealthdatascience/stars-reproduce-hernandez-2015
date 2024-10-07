# Experiment 4 (Figure 9)
# Tri-objective model with 1, 2 or 3 greeters/line managers

# Run time: 37 minutes
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
population = 50
generations = 25
lowerBounds = [1, 1, 1, 1]

# Path to save results
experimentFolder = '../python_outputs/experiment4'

# Scenarios to run for this experiment
scenarios = [
    {
        'upperBounds': [1, 60, 60, 60],
        'solutionpath': join(experimentFolder, '1_line_manager')
    },
    {
        'upperBounds': [2, 60, 60, 60],
        'solutionpath': join(experimentFolder, '2_line_managers')
    },
    {
        'upperBounds': [3, 60, 60, 60],
        'solutionpath': join(experimentFolder, '3_line_managers')
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
     'population': population,
     'generations': generations,
     'objectiveTypes': objectiveTypes,
     'solutionpath': scenario['solutionpath'],
     'lowerBounds': lowerBounds,
     'upperBounds': scenario['upperBounds']}
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
