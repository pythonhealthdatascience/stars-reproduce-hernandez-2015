import datetime
from os import listdir
from os.path import isfile, join
import os, inspect, sys

import ParameterReader
import SolutionWriter
import ExperimentRunner

startTime = datetime.datetime.now()

mypath = r'./experiments-to-run'
experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
seeds = [123, 456, 789]

# Select the first file (rather than doing a loop)
experimentFile = experimentFiles[0]
print(experimentFile)

# Create an instance of the parameter read class
parameterReader = ParameterReader.ParameterReader(join(mypath,experimentFile))
print(vars(parameterReader))

# Create an instance of the experiment runner class
experimentRunner = ExperimentRunner.ExperimentRunner(seeds, parameterReader)
print(vars(experimentRunner))

print('Experiment runner')
experimentRunner.run(runs=1, population=100, generations=5)
endTime = datetime.datetime.now()
print 'time elapsed =', endTime - startTime

print('Solution writer')
solutionWriter = SolutionWriter.SolutionWriter(join(mypath,experimentFile),experimentRunner)
endTime = datetime.datetime.now()
print 'time elapsed =', endTime - startTime

print('Solution writer dump')
solutionWriter.dumpSolution()
endTime = datetime.datetime.now()
print 'time elapsed =', endTime - startTime