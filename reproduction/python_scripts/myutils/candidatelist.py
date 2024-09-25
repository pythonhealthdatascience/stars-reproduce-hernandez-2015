'''
Created on Aug 20, 2012

@author: ivihernandez
'''
"""
    This class is an extension of python's list class.
    The extension is that the list also has an associated
    hash table that maps demand centers to its assigned distribution center.
"""
import myutils
import copy
class Candidatelist(list):
    """
    def __init__(self,mylist):
        list.__init__(self)
        self.mymap = None
        self.interdictionStrategy = None
    """
    def set_map(self, mymap):
        self.mymap = mymap.copy()
        #self.mymap = copy.copy(mymap)
    def get_map(self):
        try:
            theCopy = copy.copy(self.mymap)
        except Exception:
            return {}
        return theCopy
    
    def set_chromosome_after_interdiction(self, chromosome):
        self.interdictedFacilities = chromosome
    def get_chromosome_after_interdiction(self):
        return self.interdictedFacilities
    