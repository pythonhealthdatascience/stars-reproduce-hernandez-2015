'''
Created on Feb 18, 2011

@author: ivihernandez

'''

"""
from ecspy import emo
from ecspy import variators
from ecspy import terminators
"""


#ivan's imports
import mopsda
import myutils
"""
from mopsda import *
from myutils import *
"""
def psda(prng, popSize, generations, problem, seeds=[] ):
    """
        Determine if PSDA-integer or PSDA-binary should be called.
        @param prng: object for random number generation
        @param pop_size: size of the population
        @param generations: number of generations to evolve
        @param problem: description of the optimization problem 
        (FOM, objective functions)
        @param seeds: initial set of candidate solutions 
        @return: archive of the Pareto set  
    """
    if problem.__class__.__name__=="CapacitatedFacilityLocationProblem":
        return psda_integer(prng, popSize, generations, problem, seeds)
    else:
        return psda_binary(prng, popSize, generations, problem, seeds)
def psda_integer(prng, popSize, generations, problem, seeds=[] ):
    
    ea = mopsda.MOPSDA(prng)
        
        
    final_pop = ea.evolve_integer(
                          generator = problem.generator, 
                          evaluator=problem.evaluator, 
                          popSize=popSize,
                          maximize=problem.maximize,
                          maxGenerations=generations,
                          indLength=problem.dimensions,
                          seeds=seeds,
                          problem=problem)
    
    #sort the population
    ea.archive.sort(cmp=myutils.individual_compare)
    return ea

def psda_binary(prng, popSize, generations, problem, seeds=[] ):
    
    ea = mopsda.MOPSDA(prng)
    
    
        
    finalPop = ea.evolve_binary(
                          generator = problem.generator, 
                          evaluator=problem.evaluator, 
                          popSize=popSize,
                          maximize=problem.maximize,
                          maxGenerations=generations,
                          indLength=problem.dimensions,
                          seeds=seeds,
                          problem=problem)
    
    #sort the population
    ea.archive.sort(cmp=myutils.individual_compare)
    return ea