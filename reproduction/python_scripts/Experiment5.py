# Experiment 5 (Figure 10)
# 6 dispensing, 6 screening, 4 line manager, 1 medical evaluator
# Number of replications 1-7

# Run time: TODO add runtime
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os.path import join
import datetime
import sys
sys.path.append('./myutils')
import myutils
import PODSimulation
import ResultsAnalyzer

# Path to save results
experimentFolder = '../python_outputs/experiment5'

# Code adapted from PODSimulation.py...

def get_20_seeds():
    seeds = [2308947, 
             982301, 
             329, 
             12389, 
             34324,
             45645,
             45456546,
             681683,
             7,
             543,
             3982473289,
             1321,
             798789,
             8809,
             35797,
             43,
             879,
             32432,
             78987,
             675489]
    return seeds

# Start timer
startTime = datetime.datetime.now()

capacities = [4, 6, 6, 1]

seeds = get_20_seeds()

simulations = []
for seed in seeds:
    # Run simulation
    simul = PODSimulation.PODSimulation(capacities)
    simul.model(seed)
    # Save throughput from each run to a list
    simulations.append(simul.get_number_out())

# Save results to file
with open(join(experimentFolder, "results.txt"), "w") as text_file:
    text_file.write(str(simulations))

# End timer and save time for that result
endTime = datetime.datetime.now()
with open(join(experimentFolder, "time.txt"), "w") as text_file:
    text_file.write("{0}".format(endTime - startTime))