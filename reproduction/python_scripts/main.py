# Main script to run model for specified scenarios

import datetime
import os
from os.path import join
import ParameterReader
import SolutionWriter
import ExperimentRunner
from multiprocessing import Pool


def run_scenario(mypath, experimentFolder, file, runs, population,
                 generations, objectiveTypes):
    '''
    Run algorithm using the pre-screened percentage from the provided file.

    Parameters:
    ----------
    mypath : string
        Path to scenarios
    experimentFolder : string
        Path to save results
    file : string
        Path to text file containing pre-screened percentage
    runs : integer
        Number of times to repeat analysis
    population: integer
        Size of population
    generations : integer
        Number of generations
    objectiveTypes : list
        List of booleans which define whether maximise/minimise 2/3 objectives
    '''
    # Seeds for reproducibility
    seeds = [123, 456, 789]

    # Run the analysis
    parameterReader = ParameterReader.ParameterReader(join(mypath,
                                                           file))
    experimentRunner = ExperimentRunner.ExperimentRunner(seeds,
                                                         parameterReader,
                                                         objectiveTypes)
    experimentRunner.run(runs=runs,
                         population=population,
                         generations=generations)

    # Get the pre-screened percentage for that scenario and folder
    scenario = int(parameterReader.parameters['preScreenedPercentage']*100)
    scenarioFolder = experimentFolder + '/prescreen' + str(scenario)

    # Save the results
    solutionWriter = SolutionWriter.SolutionWriter(
        os.path.join(mypath, file), experimentRunner,
        folderName=scenarioFolder)
    solutionWriter.dumpSolution()


def wrapper(d):
    '''
    Wrapper function to allow input of dictionary tp Pool() for run_scenario()

    Parameters:
    -----------
    d : dictionary
        Dictionary containing parameters to input to run_scenario()
    '''
    return run_scenario(**d)


def run_experiment(mypath, experimentFolder, experimentFiles, runs, population,
                   generations, objectiveTypes):
    '''
    Run set of scenarios using parallel processing, and record time elapsed

    Parameters:
    -----------
    mypath : string
        Path to scenarios
    experimentFolder : string
        Path to save results
    experimentFiles : list
        List where each element is a string path to a text file containing a
        pre-screened percentage
    runs : integer
        Number of times to repeat analysis
    population: integer
        Size of population, representing number of individuals in each
        generation
    generations : integer
        Number of generations to run algorithm for, which determines how long
        algorithm will evolve for solutions
    objectiveTypes : list
        List of booleans which define whether maximise/minimise 2/3 objectives
    '''
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
         'objectiveTypes': objectiveTypes}
        for file in experimentFiles
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
