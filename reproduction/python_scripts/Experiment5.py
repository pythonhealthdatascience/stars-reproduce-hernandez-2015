# Experiment 5 (Figure 10)
# Tri-objective model with 6 dispensing, 6 screening, 4 line manager,
# one medical evaluator, number of replications 1-7

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
objectiveTypes = [False, True, False]
population = 100
generations = 1

# Greeter, screener, dispenser, medic
lowerBounds = [4, 6, 6, 1]
upperBounds = [4, 6, 6, 1]

# Path to save results
experimentFolder = '../python_outputs/experiment5'

# Scenarios to run for this experiment
scenarios = []
for i in range(1, 8):  # Loop from 1 to 7
    scenarios.append({
        'runs': i,
        'solutionpath': join(experimentFolder, str(i) + 'run')
    })

# Start timer
startTime = datetime.datetime.now()

# Create parameter list for each experiment
params = [
    {'mypath': mypath,
     'experimentFolder': experimentFolder,
     'file': file,
     'runs': scenario['runs'],
     'population': population,
     'generations': generations,
     'objectiveTypes': objectiveTypes,
     'solutionpath': scenario['solutionpath'],
     'lowerBounds': lowerBounds,
     'upperBounds': upperBounds}
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
