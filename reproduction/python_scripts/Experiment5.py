# Experiment 5 (Figure 10)
# 6 dispensing, 6 screening, 4 line manager, 1 medical evaluator
# Number of replications 1-7

# Run time: TODO add runtime
# (Intel Core i9-13900K with 81GB RAM running Pop!_OS 22.04 Linux)

from os.path import join
import sys
sys.path.append('./myutils')
import myutils
import ParameterReader
import SimulatorRunner
import StaffAllocationProblem

# Set capacities
capacities = [4, 6, 6, 1]

# Seeds as in main.py
seeds = [123, 456, 789]

# Get pre-screening parameter as in main.py
mypath = r'../inputs'
file = '10-prescreened.txt'
parameterReader = ParameterReader.ParameterReader(join(mypath, file))

# Code to run simulation as from StaffAllocationProblem.py
simulatorRunner = SimulatorRunner.SimulatorRunner()
simulatorRunner.run(seeds=seeds,
                    capacities=capacities,
                    parameterReader=parameterReader)
time = simulatorRunner.get_avg_waiting_times()
resources = simulatorRunner.get_resource_count()
throughput = simulatorRunner.get_processed_count()

# Print results
print(time)
print(resources)
print(throughput)