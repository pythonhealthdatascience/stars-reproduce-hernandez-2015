'''
Created on Feb 18, 2011

@author: ivihernandez
'''
#standard imports
import time
import collections
#non standard imports
import inspyred
#ivan's imports
import candidatelist

"""
from time import time
from ecspy import emo
from ecspy import variators
from ecspy import terminators
from ecspy import ec

from random import *
from collections import defaultdict
"""

class MOPSDA(inspyred.ec.EvolutionaryComputation):
    def __init__(self, prng):
        inspyred.ec.EvolutionaryComputation.__init__(self, prng)
        self.population = []
        self.archive = []
        self.finalArchive = []
        self.prng = prng
        
    def get_initial_pie(self, problem):
        """
            To be used only by Intger PSDA.
            
            @param : None
            @return: a vector of probabilities for each chromosome
                i.e, with equal probabilities, for a range of 3, 
                    this would be:
                    [0.333, 0.333, 0.333 ]
        """
        lowerBound = problem.lowerBound
        upperBound = problem.upperBound
        range = (upperBound - lowerBound) + 1
        share = 1/float(range)
        v = collections.defaultdict(int)
        z = xrange(lowerBound, upperBound + 1)
        for i in z:
            v[i] = share
        return v
        
        
    def get_chromosome_probability_pie(self, v):
        """
            To be used only by Integer PSDA
            @param v: chromosome probability distribution for integers
                i.e, 0 -> 0.5
                     1 -> 0.3
                     2 -> 0.2
            @return: the probability bounds of each distribution center 
                i.e, 0 -> (0,   0.5)
                     1 -> (0.5, 0.8)
                     2 -> (0.8, 1.0)
            get the probability pie, so that when a random
            number in [0,1] gets generated, we know which
            integer value should we create
        """
        
        bounds = {}
        lower = 0
        for dc, prob in v.iteritems():
            upper = lower + prob
            bounds[dc] = (lower, upper)
            lower = upper
        return bounds
    """
    def evole(self, generator, evaluator, maximize, pop_size, max_generations, ind_length, seeds, problem):
            print "calling evolve", problem.chromosomeType
            chromosomeType = problem.chromosomeType
            if chromosomeType=="binary":
                return self.evolve_binary(generator, evaluator, maximize, pop_size, max_generations, ind_length, seeds)
            elif chromosomeType=="integer":
                return self.evolve_integer(generator, evaluator, maximize, pop_size, max_generations, ind_length, seeds)
    """
    def evolve_integer(self, generator, evaluator, maximize, popSize, maxGenerations, indLength, problem, seeds):
            """
            if seeds == []:
                gamma = [0]*ind_length#gamma[chromosomeIndex][chromosomeValue]
                #generate initial probabilities
                for i in range(ind_length):
                    gamma[i] = self.get_initial_pie(problem)
            else:
                #use the seeds to create an initial gamma
                initial_pop = seeds
                initial_fits = evaluator(candidates=initial_pop, args=None)
                for elem, fit in zip(initial_pop, initial_fits):
                    ind = ec.Individual(elem)
                    ind.fitness = fit
                    self.population.append(ind)
                #print "initial_pop",initial_pop
                #remove dominated
                self.archiver = ec.archivers.best_archiver
                self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
                
                #print "archive",self.archive
                #add current non-dominated to the final list of non-dominated ones
                self.final_archive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.final_archive), args=None)
                #update gamma
                
                gamma = [0]*ind_length #gamma[chromosomeIndex][chromosomeValue]
                for i in range(len(gamma)):
                    gamma[i] = defaultdict(int)
                weight =1/float(len(self.archive))
                for ind in self.final_archive:
                    chromosome = ind.candidate
                    for index, element in enumerate(chromosome):
                        gamma[index][element] += weight
            """
            if seeds != []:
                initialPop = seeds
                
                initialFits = evaluator(candidates=initialPop, args=None)
                for elem, fit in zip(initialPop, initialFits):
                    ind = inspyred.ec.Individual(elem)
                    ind.fitness = fit
                    self.population.append(ind)
                #print "initial_pop",initial_pop
                #remove dominated
                self.archiver = inspyred.ec.archivers.best_archiver
                self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
                
                #print "archive",self.archive
                #add current non-dominated to the final list of non-dominated ones
                self.finalArchive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.finalArchive), args=None)
            
            
            #traditional integer PSDA
            gamma = [0] * indLength#gamma[chromosomeIndex][chromosomeValue]
            #generate initial probabilities
            for i in range(indLength):
                gamma[i] = self.get_initial_pie(problem)
            
            for u in range(maxGenerations):
                initial_pop = []
                
                for g in range(popSize):
                    
                    ind = []
                    for i in range(indLength):
                        
                        pie = self.get_chromosome_probability_pie(gamma[i])
                        prob = self.prng.random()
                        #print "pie",pie, "prob",prob
                        for chromosomeValue, bound in pie.iteritems():
                            (lower, upper) = bound
                            if prob >= lower and prob < upper:
                                ind.append(chromosomeValue)
                    
                    initialPop.append(ind)
                
                initialFits = evaluator(candidates=initialPop, args=None)
        
                for elem, fit in zip(initialPop, initialFits):
                    ind = inspyred.ec.Individual(elem)
                    ind.fitness = fit
                    self.population.append(ind)
                
                #remove dominated
                self.archiver = inspyred.ec.archivers.best_archiver
                self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
                
                #add current non-dominated to the final list of non-dominated ones
                self.finalArchive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.finalArchive), args=None)
                    
                #update gamma
                gamma = [0] * indLength #gamma[chromosomeIndex][chromosomeValue]
                for i in range(len(gamma)):
                    gamma[i] = collections.defaultdict(int)
                weight =1/float(len(self.archive))
                for ind in self.final_archive:
                    chromosome = ind.candidate
                    for index, element in enumerate(chromosome):
                        gamma[index][element] += weight
                
                #check for early termination
                finished = True
                for value in gamma:
                    for elem in value:
                        if elem != 0.0 or elem != 1.0:
                            finished = False
                            break 
                    if not finished:
                        break
                if finished:
                    break
            
            self.archive = self.final_archive
            return self.archive 
            
    def evolve_binary(self, generator, evaluator, maximize, popSize, maxGenerations, indLength, problem, seeds):
        # @arg evaluator: comes from problem.evaluator, function that determines the figures of merit
        # @arg maximize: list of booleans that determine if an objective function should be maximized or not (minimized)
        # @arg pop_size: size of the population per generation
        # @arg max_generations: maximum number of iterations to be performed by the EA
        # @arg ind_lenght: size of the chromosome
        # @arg seeds: iterable collection of candidate solutions to include
        
        
        random = self.prng
        initialPop = seeds
        """
        if initial_pop != []:
            #seeds were received as argument
            
            #evaluate all individuals generated
                            
            initial_fits = evaluator(candidates=initial_pop, args=None)
            for elem, fit in zip(initial_pop, initial_fits):
                ind = ec.Individual(elem)
                ind.fitness = fit
                self.population.append(ind)
            
            #remove dominated
            self.archiver = ec.archivers.best_archiver
            self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
            
            
            #add current non-dominated to the final list of non-dominated ones
            self.final_archive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.final_archive), args=None)
            
            
            
            #update gamma
            gamma = [0]*ind_length    
            weight = 1.0/len(self.final_archive)
            for ind in self.final_archive:
                for j in xrange(ind_length):
                    if ind.candidate[j] == 1:
                        gamma[j] += weight
        else:
            #no seeds received, running traditional psda with lambda = 0.5
            gamma = [0.5]*ind_length
        """
        
        
        
        
        if initialPop != []:
            initialFits = evaluator(candidates=initialPop, args=None)
            for elem, fit in zip(initialPop, initialFits):
                ind = inspyred.ec.Individual(elem)
                ind.fitness = fit
                self.population.append(ind)
            
            #remove dominated
            self.archiver = inspyred.ec.archivers.best_archiver
            self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
            
            
            #add current non-dominated to the final list of non-dominated ones
            self.finalArchive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.finalArchive), args=None)
        
        #traditional PSDA
        #######################################################
        gamma = [0.5] * indLength
        
        
        for u in xrange(maxGenerations):
            
            initialPop = []
            #self.population = []
            for i in xrange(popSize):
                elem = candidatelist.Candidatelist()
                for j in xrange(indLength):
                    if random.random() < gamma[j]:
                        elem.append(1)
                    else:
                        elem.append(0)
                initialPop.append(elem)
                
            initialFits = evaluator(candidates=initialPop, args=None)
        
            for elem, fit in zip(initialPop, initialFits):
                ind = inspyred.ec.Individual(elem)
                ind.fitness = fit
                self.population.append(ind)
            
            #remove dominated
            self.archiver = inspyred.ec.archivers.best_archiver
            self.archive = self.archiver(random=self.prng, population=list(self.population), archive=list(self.archive), args=None)
            
            #add current non-dominated to the final list of non-dominated ones
            self.finalArchive = self.archiver(random=self.prng, population = list(self.archive), archive=list(self.finalArchive), args=None)
                
            #update gamma
            gamma = [0] * indLength    
            weight = 1.0/len(self.finalArchive)
            for ind in self.finalArchive:
                for j in xrange(indLength):
                    if ind.candidate[j] == 1:
                        gamma[j] += weight
        
            #check for early termination
            finished = True
            for value in gamma:
                if value != 0.0 or value != 1.0:
                    finished = False
                    break 
            if finished:
                break
            
        #print gamma
        
        #Note: the most important part of the algorithm might be
        #the initialization step

        #Other EAs return the population, PSDA should return the final archive
        self.archive = self.finalArchive
        #return self.archive 
        
        #uncomment the previous line
        return self.population
        
        #old code ->            
        #return list(self.final_archive)
     
"""    
if __name__ == "__main__":
    prng = Random()
    mopsda = MOPSDA(prng)
"""    
        
