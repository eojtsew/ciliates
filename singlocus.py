# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 18:05:00 2014

@author: joe
"""

import numpy as np

class Single_locus:
    """Each instance represents a haploid individual with a single locus"""
    
    def __init__(self,w=1):
        """Initialize haploid, single locus individual"""
        self.fitness = w
        
    def __repr__(self):
        """"""
        return str(self.fitness)
    
    def mutate(self,mu,s):
        """Mutate with probability mu and selection coefficient s"""
        if np.random.binomial(1,mu) == 1:
            self.fitness = self.fitness + s
            
    def reproduce(self):
        """Produce offspring"""
        offspring = Single_locus(self.fitness)
        return offspring
    

#class SLpopulation:
    #"""Population of haploid individuals (single-locus)"""
    #def __init__(self,N,Ws=None):
        #""""""
        #self.N = N
        #if Ws == None:
            #self.orgs = np.ones(self.N)
        #else:
            #self.orgs = np.array(Ws)
        #self.orgs = map(Single_locus,self.orgs)
        #self.alleles = self.set_alleles()
        
    #def set_alleles(self):
        #"""Return an array of unique alleles and corresponding frequencies"""
        #allele_Ws = self.orgs.unique()

        
def next_generation(self,how="mult"):
        """...validate..."""
        self.mutations()
        self.reproduction()
        w = self.get_fitnesses(how)
        cumul_w = np.cumsum(w)
        rand_arr = np.random.sample(self.N)
        rand_arr = rand_arr*cumul_w[self.N-1]
        indices = np.searchsorted(cumul_w,rand_arr,side='left')
        next_gen = []
        for i in range(self.N):
            next_gen.append(self.orgs[indices[i]].reproduce())
        self.orgs = np.array(next_gen)
        self.generation += 1            
        
        
        
        
        
        
        
        