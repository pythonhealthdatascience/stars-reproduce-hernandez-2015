'''
Created on May 15, 2013

@author: ivihernandez
'''
#standard imports
import datetime
import os.path
import ntpath
import shutil
import time
import os


class SolutionWriter:

    def __init__(self, experimentFilePath, experimentRunner, folderName=None):
        """
            @param experimentFilePath: path to the file that generated the results 
            @param experimentRunner: object that contains the results of the experiment
            @param folderName: string with path to folder to save results into (optional, defaults to date+time)
             
        """
        self.experimentFilePath = experimentFilePath
        self.experimentRunner = experimentRunner
        if folderName:
            self.folderName = folderName
        else:
            self.folderName = time.strftime("../python_outputs/%a %d %b %Y %H %M %S", time.gmtime())

    def dumpResultsAnalyzer(self):
        #os.mkdir(self.folderName)
        experimentFileName = os.path.basename(self.experimentFilePath)
        #print self.folderName, experimentFileName
        destinationFilePath = os.path.join(self.folderName, experimentFileName)
        
        #copy original experiment
        #shutil.copy(self.experimentFilePath, destinationFilePath)
        #copy results
        
        
        
        pareto = self.experimentRunner.get_pareto()
        index = 1
        for solution in pareto:
            resultsFile = 'results-' + str(index) + '.txt'
            filePareto = open(os.path.join(self.folderName, resultsFile), 'w')
            fitness = solution.fitness
            values = fitness.values
            resultsString = str(values)
            filePareto.write(resultsString)
            resultsAnalyzer = values.get_results_analyzer()
            resultsString = str(resultsAnalyzer)
            filePareto.write(resultsString)
            filePareto.close()
            index = index + 1

    def dumpSolution(self):
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
        experimentFileName = os.path.basename(self.experimentFilePath)
        #print folderName, experimentFileName
        destinationFilePath = os.path.join(self.folderName, experimentFileName)
        
        #copy original experiment
        #shutil.copy(self.experimentFilePath, destinationFilePath)
        #copy results
        
        resultsFile = 'results.txt'
        filePareto = open(os.path.join(self.folderName, resultsFile), 'w')
        pareto = self.experimentRunner.get_pareto()
        firstLine = ""
        firstLine += 'greeter'
        firstLine += '\tscreener'
        firstLine += '\tdispenser'
        firstLine += '\tmedic'
        firstLine += '\tresources'
        firstLine += '\tthroughput'
        firstLine += '\ttime'
        filePareto.write(firstLine + "\n")
        for solution in pareto:
            #filePareto.write(str(solution) + "\n")
            chromosome = solution.candidate
            fitness = solution.fitness
            
            line = ''
            for index, element in enumerate(chromosome):
                if index >= 1:
                    line += '\t'
                line += str(element)
            for index, element in enumerate(fitness):
                line += '\t'
                line += str(element)
            filePareto.write(line + '\n')
        filePareto.close()
         
        #self.dumpResultsAnalyzer()
        