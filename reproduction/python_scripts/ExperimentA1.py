# Experiment for Appendix A.1 (Table 3)
# 6 dispensing, 6 screening, 4 line manager, 1 medical evaluator
# Number of replications 20

# Run time: 9 seconds
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os.path import join
import datetime
import csv
import sys
sys.path.append('./myutils')
import myutils
import PODSimulation
import ResultsAnalyzer

# Path to save results
experimentFolder = '../python_outputs/experimenta1'

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

# Parameters
capacities = [4, 6, 6, 1]
seeds = get_20_seeds()

# Run simulations
simulations = []
for seed in seeds:
    simul = PODSimulation.PODSimulation(capacities)
    simul.model(seed)
    simulations.append(simul)
resultsAnalyzer = ResultsAnalyzer.ResultsAnalyzer(simulations)

# Create results table
data = [
    ['Wait time', resultsAnalyzer.avgTotalWaitingTime,
     resultsAnalyzer.halfWidthTotalWaitingTime],
    ['No. in (Designees)', resultsAnalyzer.avgTotalNumberIn,
     resultsAnalyzer.halfWidthTotalNumberIn],
    ['No. out (Designees)', resultsAnalyzer.avgTotalNumberOut,
     resultsAnalyzer.halfWidthTotalNumberOut],
    ['Dispensing wait time', resultsAnalyzer.waiting['dispenser'],
     resultsAnalyzer.halfWidthWaitingTimes['dispenser']],
    ['Line mngr. wait time', resultsAnalyzer.waiting['greeter'],
     resultsAnalyzer.halfWidthWaitingTimes['greeter']],
    ['Med. eval. wait time', resultsAnalyzer.waiting['medic'],
     resultsAnalyzer.halfWidthWaitingTimes['medic']],
    ['Screening wait time', resultsAnalyzer.waiting['screener'],
     resultsAnalyzer.halfWidthWaitingTimes['screener']],
    ['Dispensing no. waiting', resultsAnalyzer.numberWaiting['dispenser'],
     resultsAnalyzer.halfWidthNumberWaiting['dispenser']],
    ['Line mngr. no. waiting', resultsAnalyzer.numberWaiting['greeter'],
     resultsAnalyzer.halfWidthNumberWaiting['greeter']],
    ['Med. eval. no. waiting', resultsAnalyzer.numberWaiting['medic'],
     resultsAnalyzer.halfWidthNumberWaiting['medic']],
    ['Screening no. waiting', resultsAnalyzer.numberWaiting['screener'],
     resultsAnalyzer.halfWidthNumberWaiting['screener']]
]

# Save to csv
with open(join(experimentFolder, 'results.csv'), 'w') as file:
    writer = csv.writer(file)
    # Write header (optional)
    writer.writerow(['Estimate', 'Avg', 'HalfWidth'])
    # Write data
    writer.writerows(data)

# End timer and save time for that result
endTime = datetime.datetime.now()
with open(join(experimentFolder, "time.txt"), "w") as text_file:
    text_file.write("{0}".format(endTime - startTime))
