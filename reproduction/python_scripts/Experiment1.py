# Experiment 1
# Run with a population of 100 and 50 generations
# Alter percentage of pre-screened (10%, 20%, 30%,... 90%)
# Used to produce Figure 5 and 6

# Import required libraries 
import datetime
from os import listdir
from os.path import isfile, join
import os, sys
import ParameterReader
import SolutionWriter
import ExperimentRunner
from multiprocessing import Pool

# Path to scenarios
mypath = r'../inputs'
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Path to save results
experimentFolder = '../python_outputs/experiment1'

# Seeds for reproducibility
seeds = [123, 456, 789]


def run_scenario(file):
    '''
    Run algorithm using the pre-screened percentage from the provided file.

    Parameters:
    ----------
    file : string
      Path to text file containing pre-screened percentage
    '''
    # Run the analysis
    parameterReader = ParameterReader.ParameterReader(join(mypath,
                                                           file))
    experimentRunner = ExperimentRunner.ExperimentRunner(seeds,
                                                         parameterReader)
    experimentRunner.run(runs=1,
                         population=50,
                         generations=25)

    # Get the pre-screened percentage for that scenario and folder
    scenario = int(parameterReader.parameters['preScreenedPercentage']*100)
    scenarioFolder = experimentFolder + '/prescreen' + str(scenario)

    # Save the results
    solutionWriter = SolutionWriter.SolutionWriter(
        join(mypath, file), experimentRunner,
        folderName=scenarioFolder)
    solutionWriter.dumpSolution()


# Start timer
startTime = datetime.datetime.now()

# Create a process pool that uses all CPUs
pool = Pool()
try:
    # Map the run_scenario function to the experiment files
    results = pool.map(run_scenario, experimentFiles)
finally:
    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()

# End timer and save time for that result
endTime = datetime.datetime.now()
with open(os.path.join(experimentFolder, "time.txt"), "w") as text_file:
    text_file.write("{0}".format(endTime - startTime))
