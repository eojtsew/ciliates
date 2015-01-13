# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 03:18:28 2015

@author: paulwest
"""

import numpy as np
from numpy import random

class Genome:
    """"""
    def __init__(self,L,P,K=None):
        """"""
        if K != None:
            self.K = K
        else:
            self.K = np.zeros(L,dtype='int64')
        self.P = P
        self.L = L
        
    def __repr__(self):
        return str(self.K)
        
    def mutate(self,mu):
        """"""
        n = self.P - self.K
        mutations = np.random.binomial(n,mu)
        self.K += mutations
        
    def mitosis(self):
        """"""
        daughter = Genome(self.L,self.P,np.array(self.K))
        return daughter
        
    #broken...
    def amitosis(self):
        """"""
        k = 2*(self.P - self.K)
        wt = 2*self.K
        newk = np.random.hypergeometric(wt,k,self.P)
        daughter = Genome(self.L,self.P,(np.array((self.P-newk))))
        self.K = newk
        return daughter
        
        
        