'''
Created on Mar 29, 2011

@author: ivihernandez
'''
#standard imports
import sys
import re
import os
import random
import time
import copy
import collections

#non standard imports
import matplotlib.pyplot as plt
import networkx as nx
import pylab
import numpy as np
import inspyred
import xml.etree.cElementTree as ET
#ivan's imports
import combined
import candidatelist
"""
def copy_dictionary(thedict):
    newdict = {}
    for key, value in thedict.iteritems():
        newdict[key] = copy.deepcopy(value)
    
    k = random.randint(0,100)
    thelist = []
    for i in range(k):
        r = random.randint(0,100)
        thelist.append(r)
    return newdict
    #return thelist
"""
def get_file_name(path):
    """
        return the file name without extension, given an absolute path
    """
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]
def kill():
    print "lo mato yo",1/0

def load_pareto(paretoFilePath):
    """
        Load in memory a pareto file
        The function should determine if the values are float or int
    """
    archive = []
    tree = ET.ElementTree(file=paretoFilePath)
    objectiveTypes = []
    for elem in tree.iter(tag='objective'):
        theType = elem.attrib['type']
        if theType.lower() == 'minimize':
            objectiveTypes.append(False)
        elif theType.lower() == 'maximize':
            objectiveTypes.append(True)
        else:
            raise(Exception('unknown objective type. Only minimize and maximize'))
    for elem in tree.iter(tag='solution'):
        chromosome = []
        fitness = []
        for subelem in elem:
            if subelem.tag == 'chromosome':
                chromo = subelem.text.strip()
                chromo = chromo[1:-1]
                chromo = chromo.split(',')
                for value in chromo:
                    chromosome.append(int(value))
            if subelem.tag == 'values':
                for subsubelem in subelem:
                    if subsubelem.tag == 'function':
                        fitness.append(float(subsubelem.text))
        #new check out
        chromosome = candidatelist.Candidatelist(chromosome)
        
        ind = inspyred.ec.Individual(chromosome)
        objective_types = [False, False]
        
        fit = inspyred.ec.emo.Pareto(fitness, objective_types)
        ind.fitness = fit
        archive.append(ind)
    
    return archive

def load_pareto_distribution_centers(paretoFilePath):
    """
        @param paretoFilePath: .xml file represing a Pareto set
        @return: X, which is a list of lists.
         
        Each x_i of X is a list containing the ids of the distribution centers for
        a particular Pareto solution. len(X) = size of the Pareto. One sublist for each solution.
    """
    X = []
    archive = []
    tree = ET.ElementTree(file=paretoFilePath)
    for elem in tree.iter(tag='assignment'):
        temp = []
        for subelem in elem:
            
            if subelem.tag == 'pair':
                
                for subsubelem in subelem:
                    
                    if subsubelem.tag == 'distributionCenter':
                        temp.append(subsubelem.text.strip())
        if len(temp) == 0:
            continue
        X.append(temp)
    return X
def my_best_archiver(random, population, archive, args):
    """Archive only the best individual(s).
    
    This function archives the best solutions and removes inferior ones.
    If the comparison operators have been overloaded to define Pareto
    preference (as in the ``Pareto`` class), then this archiver will form 
    a Pareto archive.
    
    .. Arguments:
       random -- the random number generator object
       population -- the population of individuals
       archive -- the current archive of individuals
       args -- a dictionary of keyword arguments
    
    """
    
    counter = 0
    new_archive = archive
    for ind in population:
        #counter += 1
        
        if len(new_archive) == 0:
            new_archive.append(ind)
        else:
            should_remove = []
            should_add = True
            doBreak = False
            for a in new_archive:
                
                
                sameFitness = True
                for i in range(len(ind.fitness)):
                    if ind.fitness[i] != a.fitness[i]:
                        sameFitness = False
                        break
                
                sameCandidate = True
                for i in range(len(ind.candidate)):
                    if ind.candidate[i] != a.candidate[i]:
                        sameCandidate = False
                        break
                
                if sameCandidate and sameFitness:
                    should_add = False
                    break
                
                
                if not sameCandidate:
                    if ind == a:
                        should_add = False
                        doBreak = True
                    elif ind < a:
                        should_add = False
                    elif ind > a:
                        should_remove.append(a)
                else:
                    if ind < a:
                        should_add = False
                    elif ind > a:
                        should_remove.append(a)
                    
                    
                
                if doBreak:
                    break
                
            for r in should_remove:
                new_archive.remove(r)
            if should_add:
                new_archive.append(ind)
    
    
    return new_archive

def log_time(file, totalTime, avgTime, maxTime, minTime, totalEvaluations, ea):
    algoName = ea.__class__.__name__
    totalTimeLine = '\nTotal time for '+algoName+' was (min): '+ str(totalTime)
    avgTimeLine = 'Avg time for '+algoName+' was: '+ str(avgTime)
    minTimeLine = 'Min time for '+algoName+' was: '+ str(minTime)
    maxTimeLine = 'Max time for '+algoName+' was: '+ str(maxTime)
    totalEvaluationsLine = 'Total evaluations performed by '+algoName+' was: '+ str(totalEvaluations)
    print totalTimeLine
    print avgTimeLine
    print minTimeLine
    print maxTimeLine
    print totalEvaluationsLine
    summaryFile = open(file,"a")
    summaryFile.write(totalTimeLine + os.linesep)
    summaryFile.write(avgTimeLine + os.linesep)
    summaryFile.write(minTimeLine + os.linesep)
    summaryFile.write(maxTimeLine + os.linesep)
    summaryFile.write(totalEvaluationsLine + os.linesep)
    summaryFile.close()

def log_parameters(file, parameterReader, distributionCenters, demandCenters):
    summaryFile = open(file,"a")
    distributionLine = "The distribution centers file was: "+str(os.path.basename(distributionCenters))
    demandLine =  "The demand centers file was: "+str(os.path.basename(demandCenters))
    
    pop = parameterReader.get_population_size()
    gen = parameterReader.get_generations()
    runs = parameterReader.get_runs()
    genLine = "The number of generations was: "+ str(gen)
    popLine = "The size of the population was: "+ str(pop)
    runsLine = "The number of runs was: "+ str(runs)
    
    capacitatedLine = "The capacities of the distribution centers are being considered? "
    if parameterReader.capacitated:
        capacitatedLine += "Yes"
    else:
        capacitatedLine += "No"
    summaryFile.write(capacitatedLine + os.linesep)
    
    weightedLine = "The weights of the demand centers are being considered? "
    if parameterReader.weighted:
        weightedLine += "Yes"
    else:
        weightedLine += "No"
    summaryFile.write(weightedLine + os.linesep)
    
    #objective types
    summaryFile.write("objective types:" + os.linesep)
    objectiveTypesLines = str(parameterReader.get_objective_types())
    summaryFile.write(objectiveTypesLines + os.linesep)
    
    #objective functions
    summaryFile.write("objective functions:" + os.linesep)
    for item in parameterReader.get_objective_functions():
        summaryFile.write(item + os.linesep)
    
    
        
    
    summaryFile.write(distributionLine + os.linesep)
    summaryFile.write(demandLine + os.linesep)
    summaryFile.write(genLine + os.linesep)
    summaryFile.write(popLine + os.linesep)
    summaryFile.write(runsLine + os.linesep)
    summaryFile.close()
    
    print distributionLine
    print demandLine

def get_xml_header():
    mystr = '<?xml version=\"1.0\"?>' + os.linesep
    return mystr

def log_solution(outputFilePath, archive, algorithmName, objectiveFunctions, objectiveFunctionsTypes, attributes, additionalAttributes=None):
    
    outputFile = open(outputFilePath, "a")
    mystr = ""
    mystr = get_xml_header()
    outputFile.write(mystr)
    mystr = ""
    mystr += "<results>" + os.linesep
    mystr += '<objectives number=\"' + str(len(objectiveFunctions)) + '\">' + os.linesep
    outputFile.write(mystr)
    size = len(objectiveFunctions)
    for i in range(size):
        objectiveType = objectiveFunctionsTypes[i]
        if objectiveType:
            mytype = 'maximize'
        else:
            mytype = 'minimize' 
        objectiveFunction = objectiveFunctions[i]
        mystr = '<objective type=\"'  + mytype + '\">' + objectiveFunction + "</objective>" + os.linesep
        outputFile.write(mystr)
    mystr = "</objectives>" + os.linesep
    outputFile.write(mystr)
    mystr = '<computationalAttributes>' + os.linesep
    for key, value in attributes.iteritems():
        mystr += '<' + key + '>' + os.linesep
        mystr += str(value) 
        mystr += '</' + key + '>' + os.linesep
    mystr += '</computationalAttributes>' + os.linesep
    outputFile.write(mystr)
    #additional attributes
    if additionalAttributes != None:
        mystr = '<additionalAttributes>' + os.linesep
        for key, value in additionalAttributes.iteritems():
            mystr += '<' + key + '>' + os.linesep
            mystr += str(value) 
            mystr += '</' + key + '>' + os.linesep
        mystr += '</additionalAttributes>' + os.linesep
        outputFile.write(mystr)
    
    mystr = ""
    size = len(archive)
    mystr += '<pareto size=\"'+ str(size) + '\" '
    mystr += 'algorithm=\"' +algorithmName+'\">' + os.linesep
    outputFile.write(mystr)
    
    for solution in archive:
        mystr = ""
        mystr += "<solution>" + os.linesep 
        size = str(len(solution.candidate))
        mystr += '<chromosome lenght=\"' + size + '\">' + os.linesep
        mystr += str(solution.candidate)
        mystr += "</chromosome>" + os.linesep
        outputFile.write(mystr)
        
        
        if (len(solution.fitness) > 2) :
            #running with failures
            try:
                chromosomeAfterInterdiction = solution.candidate.get_chromosome_after_interdiction() 
                size = str(len(chromosomeAfterInterdiction))
                mystr = ""
                mystr += '<chromosomeAfterInterdiction lenght=\"' + size + '\">' + os.linesep
                mystr += str(chromosomeAfterInterdiction)
                mystr += "</chromosomeAfterInterdiction>" + os.linesep
                outputFile.write(mystr)
            except Exception:
                pass
        mystr = "<values>" + os.linesep
        outputFile.write(mystr)
        for i in range(len(objectiveFunctions)):
            mystr = ""
            mystr += '<function name=\"'+ objectiveFunctions[i] + '\">' + os.linesep
            mystr += str(solution.fitness[i]) + os.linesep
            mystr += "</function>" + os.linesep
            outputFile.write(mystr)
        mystr = "</values>" + os.linesep
        outputFile.write(mystr)
        mystr = "<assignment>" + os.linesep
        outputFile.write(mystr)
        mymap = solution.candidate.get_map()
        
        
        for key, value in mymap.iteritems():
                
                mystr = "<pair>" + os.linesep
                mystr += "<distributionCenter>" + os.linesep
                mystr += str(key)
                mystr += "</distributionCenter>" + os.linesep
                mystr += "<demandCenters>" + os.linesep
                theList = list(value)
                integerList = [int(x) for x in theList]
                mystr += str(integerList)
                    
                mystr += "</demandCenters>" + os.linesep
                mystr += "</pair>"
                outputFile.write(mystr)
        mystr = "</assignment>"
        outputFile.write(mystr)
        
        #sys.exit()
        mystr = ""
        mystr += "</solution>" + os.linesep
        outputFile.write(mystr)
    mystr = "</pareto>" + os.linesep
    outputFile.write(mystr)
    mystr = "</results>" + os.linesep
    outputFile.write(mystr)
    outputFile.close()
    
    #write simple .txt file with just the objective function
    name = get_file_name(outputFilePath)
    mydir = os.path.dirname(outputFilePath)
    name += ".txt"
    simpleFilePath = os.path.join(mydir, name)
    simpleFile = open(simpleFilePath, "w")
    top = len(objectiveFunctions)
    i = 1
    for objectiveFunction in objectiveFunctions:
        simpleFile.write(objectiveFunction)
        if i < top:
            simpleFile.write("\t")
        i = i + 1
    simpleFile.write("\n")
    
    for solution in archive:
        top = len(solution.fitness) 
        i = 1
        for fitness in solution.fitness:
            simpleFile.write(str(fitness))
            if i < top:
                simpleFile.write("\t")
            i = i + 1
        simpleFile.write("\n")
    simpleFile.close()

def get_interdicted_facilities( designStrategy, interdictionStrategy):
        #
        #    @param designStrategy: chromosome representing the defenders design strategy
        #        i.e, deployed facilities
        #    @param interdictionStrategy: chromosome representing the attackers design.
        #        A bit turned on, means the facility will be interdicted (in case it was deployed).
        #        A bit turned off, mean the facility will not be interdicted.
        #
        counter = 0
        for i in range(len(designStrategy)):
            conditionA = designStrategy[i] == 1
            conditionB = interdictionStrategy[i]==1
            if  conditionA and conditionB:
                counter += 1
        return counter 

def turn_off( original, interdictionStrategy):
        """
            This function creates a design strategy with 
            interdicted elements according to interdicted
            
            @desc: This function turns off 
            additional bits in the interdiction strategy, 
            so that only bits that are on in the orignal chromosome
            might be turned off
            
            newChromosome[i] = 1 iff original[i]=1 and interdiction[i]=0.
            newChromosome[i] = 0 Otherwise
        """
        interdicted = []
        for i in xrange(len(original)):
            if (original[i] == 1) and (interdictionStrategy[i] == 0):
                interdicted.append(1)
            else:
                interdicted.append(0)
            if (interdictionStrategy[i] == 1) and (original[i] == 0):
                interdictionStrategy[i] = 0
        return interdicted

def count_zeros(elems):
    """count the number of bits that are on
        @param: elems = list of integers between 1 and 0
        @return: integer (number of zeros in elem)
    """
    counter = 0
    for x in elems:
        if x == 0:
            counter = counter + 1
    
    return counter

def count_ones(elem):
    counter = 0
    for x in elem:
        if x == 1:
            counter += 1
    return counter


def generate_seeds(problem, prng):
    name = problem.__class__.__name__ 
    if name == "CapacitatedFacilityLocationProblem":
        return generate_integer_seeds(problem, prng)
    else:
        return generate_binary_seeds(problem, prng)
        
"""
def load_mapping_file(mappingFile):
    
        #load: facility index in the chromosome -> facility id
    
    mymap = {}
    tree = ET.ElementTree(file=mappingFile)
    for elem in tree.iter():
        if elem.tag == 'pairing':
            continue
        print elem.tag, elem.attrib
        myid = elem.attrib['id']
        index = int(elem.attrib['index']) 
        mymap[index] = myid 
    return mymap 
"""
def load_coordinates(paretoFilePath, graph):
    """
        create two lists of lists. List X and list Y.
        Each element of the list contains the coordinates of the 
        distribution centers
    """
    
    print "len(graph)",len(graph)
    paretoTree = ET.ElementTree(file=paretoFilePath)
    X = [] #list of lists x coordinates
    Y = [] #list of lists y coordinates
    for elem in paretoTree.iter():
        
        if elem.tag == 'assignment':
            facilities = 0
            xTarget = []
            yTarget = []
            for subelem in elem.iter():
                
                if subelem.tag == 'distributionCenter':
                    index = subelem.text.strip()
                    print 'myutils.py',graph.node[index], 'index',index
                    xCoord = graph.node[index]['x']
                    yCoord = graph.node[index]['y']
                    xTarget.append(xCoord)
                    yTarget.append(yCoord)
                    facilities = facilities + 1
            
            if len(xTarget) == 0:
                continue
            X.append(xTarget)
            Y.append(yTarget)
    return (X,Y)


def plot_bars(archive):
    """
        plot a Pareto in form of bars
    """
    distances = []
    ticks = []
    for f in archive:
        zeros = f.candidate.count(0)
        #remove outliers in the pareto graph
        if zeros == len(f.candidate):
            continue
        getOut = False
        for fit in f.fitness:
            if fit >= sys.maxint:
                getOut = True
                break
        if getOut:
            continue
        distances.append(f.fitness[1])
        ticks.append(str(int(f.fitness[0])))
    
    #plot
    N = len(distances)
    myrange = np.arange(N)
    width = 0.8#len(ind)#0.35
    
    
    pA = plt.bar(myrange, distances, width, color="black")
    
    #pB = plt.bar(ind, distancesGivenR, width, color="r")
    plt.ylabel("Distance")
    plt.xlabel('Facilities')
    (xmin, xmax) = plt.xlim()
    (ymin, ymax) = plt.ylim()
    #plt.title("distance before and after failure")
    plt.xticks(myrange + 0.5, ticks, rotation="vertical", size=8 )
    
    #plt.legend( (pA[0],pB[0]), ('Distance prior to failure','Distance after failure'))
    plt.ylim(ymin, 7000)
    plt.show()
    

def generate_binary_seeds(problem, prng):
    """
        @desc: Generate seeds for the evolutionary algorithms,
               seeds are iterable collections of candidate solutions 
               to include in the EA
        @arg lenght: lenght of the chromosome
        @arg prng: object to generate random numbers
    """
    lenght = problem.dimensions
    
    candidates = []
    size = lenght
    
    #add individuals with just zeros (and just ones)
    
    
    ones = [1 for i in xrange(size)]
    candidates.append(candidatelist.Candidatelist(ones))
    
    
    zeros = [0 for i in xrange(size)]
    candidates.append(candidatelist.Candidatelist(zeros))
    
    for i in xrange(size):
        zeros = [0 for j in xrange(size)]
        zeros[i] = 1
        candidates.append(candidatelist.Candidatelist(zeros))
        
        ones = [1 for j in xrange(size)]
        ones[i] = 0
        candidates.append(candidatelist.Candidatelist(ones))
    
    
    return sorted(candidates,reverse=True)
    
def generate_integer_seeds(problem, maxNumber):
    candidates = []
    lenght = problem.dimensions
    
    maxNumber = problem.upperBound  + 1
    
    #add individuals with just zeros (and just ones)
    
    for i in range(maxNumber):
        number = [i for j in xrange(lenght)]
        candidates.append(number)
    
    return candidates

def individual_compare(a,b):
    """
        @desc: compare to individuals according to their score for
        various objective functions.
        
        @param: a,b. Two individuals two compare. They are part of a population
        
        @return: True if a is less than b. The method compares
        all objective functions until one individual can be determined
        to have a smaller fit than the other.
    """
    size = len(a.fitness)
    retval = 0
    
    for i in xrange(size):
        
        if a.fitness[i] < b.fitness[i]:
            retval = -1
            
            break
        elif a.fitness[i] > b.fitness[i]:
            retval = 1
            
            break
    return retval
def combine_paretos_considering_failures(prng, problem, eas):
    """
        combines paretos in such a way, that the same chromosome
        can have different scores
    """
    population = []
    for ea in eas:
        for solution in ea.archive:
            population.append(solution)
            
    
    
    
    archive = []
    
    archive = my_best_archiver(random=prng, population=list(population), archive=list(archive), args=None)
    archive.sort(cmp=individual_compare)
    
    ea = combined.NSGA_MOPSDA(prng)
    ea.__class__.__name__ = "MOPSDA & NSGA2"
    ea.archive = archive
    
    return ea
def combine_paretos(prng, problem, eas):
    """
        @desc: This function combines a list of paretos into one big pareto
         
    """
    archiver = inspyred.ec.archivers.best_archiver
    #archiver = archiver
    
    
    map = collections.defaultdict(set) #algorithm -> set of individuals
    complete = set() #set containing the individuals of all algorithms
      
    
    
    mega_archive = []#store the pareto of the several runs
    total_population = []
    for ea in eas:
        final_archive = ea.archive
        
        algorithm = ea.__class__.__name__
        for f in final_archive:
            total_population.append(f)
            map[algorithm].add(f)
            
    mega_archive = archiver(random=prng, population=list(total_population), archive=list(mega_archive), args=None)
    #create a set with the elements of the pareto
    for f in mega_archive:
        complete.add(f)
    
     
    
    resultsFolder = problem.get_results_folder()
    totalSize = len(complete)
    attributes = {}
    for key, value in map.iteritems():
        diff = complete.difference(value)
        #diff contains elements in the TRUE pareto not due to the current algorithm
        current = len(complete) - len(diff)
        prop = current/float(totalSize)
        prop = prop * 100
        prop = "%.2f"%prop
        
        
        
        
        attributes[str(key) + 'proportion'] = str(prop)
        attributes[str(key) + 'solutions'] = str(current)
        
    
    #create any EA to store the solution for future plotting
    ea = combined.NSGA_MOPSDA(prng)
    ea.__class__.__name__ = "MOPSDA & NSGA2"
    ea.archive = mega_archive
    #sort the population
    ea.archive.sort(cmp=individual_compare)
    ea.attributes = attributes
    return ea

def interpolate(sourceRange, destinyRange, value):
    """
        This function transforms the given value from the sourceRange to its
        equivalent DestinyRange.
        @param sourceRange: tuple, range of source
        @param destinyRange: tuple, range of destiny
        @param value: value to be converted
        
        Examples: 
        interpolate ( (5,10), (10,20), 7.5 ) = 15 
        interpolate ( (5,10), (10,15), 7.5 ) = 12.5
    """
    minSource = sourceRange[0]
    maxSource = sourceRange[1]
    minDestiny = destinyRange[0]
    maxDestiny = destinyRange[1]
    
    ratio = (maxDestiny - minDestiny)/ float(maxSource - minSource)
    retval = (value - minSource)*ratio + minDestiny
    return retval


def load_paretos(folder):
    """
        @param folder: directory containing multiple Pareto archives
        (in .xml format)
        @return archives: type: list. Contains multiple Pareto archives.
        and their associated names.
    """
    archives = []
    names = []
    os.chdir(folder)
    for file in os.listdir('.'):
        if file.endswith('.xml'):
            archive = load_pareto(file)
            name = os.path.splitext(os.path.basename(file))[0]
            names.append(name)
            archives.append(archive)
    
    return (names, archives)

if __name__ == '__main__':
    paretoFolder = r'C:\Users\ivihernandez\Documents\PhD-systems-engineering\projects\facility-location-unverified\results Mon 27 Aug 2012 19 01 11-trad-actual'
    paretoFileName = 'pareto-evaluation.xml'
    paretoFilePath = os.path.join(paretoFolder, paretoFileName)
    archive = load_pareto(paretoFilePath)
    plot_bars(archive)

