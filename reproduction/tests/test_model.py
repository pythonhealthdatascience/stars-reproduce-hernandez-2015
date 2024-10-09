'''
Model testing

This module contains a test which checks whether the simulation model is
producing consistent results. This is performed for the Experiment 5 model,
which just runs the simulation (and does not include the evolutionary
algorithms, which have the long run times).
'''

# Required packages
import ast
import numpy as np
import pytest
import sys

# Local imports
sys.path.append('..')
from python_scripts import PODSimulation
sys.path.append('../python_scripts/myutils')

# Path to file with expected results and to store test run results
EXP_FILE = 'exp_results/experiment_5_results.txt'


# Create fixture with path to file with expected results
@pytest.fixture
def exp_file():
    return EXP_FILE


def test_equal_df(exp_file):
    '''
    Test that model results with the default/provided input parameters are
    consistent with expected results for Experiment 5.
    '''

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

    # Set parameters (capacities and seeds)
    capacities = [4, 6, 6, 1]
    seeds = get_20_seeds()

    # Run simulation
    simulations = []
    for seed in seeds:
        # Run simulation
        simul = PODSimulation.PODSimulation(capacities)
        simul.model(seed)
        # Save throughput from each run to a list
        simulations.append(simul.get_number_out())

    # Import the expected results
    with open(exp_file, "r") as file:
        # Read the string list and convert into list type
        exp_result = ast.literal_eval(file.read())

    # Compare the results (each are a list with 20 throughput values)
    assert np.array_equal(np.array(simulations), np.array(exp_result))
