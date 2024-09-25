'''
Created on Sep 13, 2011

@author: ivihernandez
'''
from time import time

import inspyred




class NSGA_MOPSDA(inspyred.ec.EvolutionaryComputation):
    def __init__(self, prng):
        inspyred.ec.EvolutionaryComputation.__init__(self, prng)
        