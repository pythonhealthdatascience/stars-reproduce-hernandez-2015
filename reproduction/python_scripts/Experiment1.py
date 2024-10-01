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

# Path to scenarios
mypath = r'../inputs'
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Path to save results
experimentFolder = '../python_outputs/experiment1/prescreen'

# Seeds for reproducibility
seeds = [123, 456, 789]

# Loop through each of the scenarios
for experimentFile in experimentFiles:

    # Start timer
    startTime = datetime.datetime.now()

    # Run the analysis
    parameterReader = ParameterReader.ParameterReader(join(mypath,experimentFile))
    experimentRunner = ExperimentRunner.ExperimentRunner(seeds, parameterReader)
    experimentRunner.run(runs=1,
                         population=100,
                         generations=5)

    # Get the pre-screened percentage for that scenario and folder
    scenario = int(parameterReader.parameters['preScreenedPercentage']*100)
    scenarioFolder = experimentFolder + str(scenario)

    # Save the results
    solutionWriter = SolutionWriter.SolutionWriter(
        join(mypath,experimentFile), experimentRunner,
        folderName=scenarioFolder)
    solutionWriter.dumpSolution()
    #solutionWriter.dumpResultsAnalyzer()

    # End timer and save time for that result
    endTime = datetime.datetime.now()
    with open(os.path.join(scenarioFolder, "time.txt"), "w") as text_file:
        text_file.write("{0}".format(endTime - startTime))
