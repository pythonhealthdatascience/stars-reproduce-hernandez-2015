'''
Created on Feb 18, 2011

@author: ivihernandez
'''
from time import time
from inspyred.ec import emo
from inspyred.ec import variators
from inspyred.ec import terminators

#ivan's imports
from myutils import *

def nsga2(prng, popSize, generations, problem, seeds=[]):
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
        return nsga2_integer(prng, popSize, generations, problem, seeds)
    else:
        return nsga2_binary(prng, popSize, generations, problem, seeds)
def nsga2_binary(prng, popSize, generations, problem, seeds=[]):
    
    ea = emo.NSGA2(prng)
    
    #ea.variator = [variators.simulated_binary_crossover, variators.bit_flip_mutation]
    
    ea.variator = [variators.bit_flip_mutation]
    #ea.variator = variators.bit_flip_mutation
    ea.terminator = terminators.generation_termination
    
    final_pop = ea.evolve(generator=problem.generator, 
                          evaluator=problem.evaluator, 
                          popSize=popSize,
                          maximize=problem.maximize,
                          bounder=problem.bounder,
                          maxGenerations=generations,
                          seeds=seeds)
    
    #sort the population
    ea.archive.sort(cmp=individual_compare)
    
    return ea

def nsga2_integer(prng, popSize, generations, problem, seeds=[]):
    ea = emo.NSGA2(prng)
    
    ea.terminator = terminators.generation_termination
    ea.variator = [variators.n_point_crossover]
    
    final_pop = ea.evolve(generator=problem.generator, 
                          evaluator=problem.evaluator, 
                          pop_size=popSize,
                          maximize=problem.maximize,
                          bounder=problem.bounder,
                          max_generations=generations,
                          seeds=seeds)
    
    #sort the population
    ea.archive.sort(cmp=individual_compare)
    
    return ea
