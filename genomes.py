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
        
    def amitosis(self):
        """"""
        good = self.P - self.K
        #print "number wt alleles: ", good
        bad = self.K
        #print "number mutant alleles: ", bad
        #print "replication..."
        two_good = 2*good
        #print "number wt alleles: ", two_good
        two_bad = 2*bad
        #print "number mutant alleles: ", two_bad
        new_k_a = np.random.hypergeometric(two_bad,two_good,self.P)
        #print "daughter A mutant alleles: ", new_k_a
        new_k_b = two_bad - new_k_a
        #print "daughter B mutant alleles: ", new_k_b
        self.K = new_k_a
        #print "now I look like: ", self.K
        daughter = Genome(self.L,self.P,new_k_b)
        return daughter
        
    def meiosis(self):
        """"""
        hap_k = np.random.hypergeometric(self.K,(self.P - self.K),1)
        haploid = Genome(self.L,1,hap_k)
        return haploid
        
    def fertilization(self,other):
        """"""
        diploid_k = self.K + other.K
        zygote = Genome(self.L,(self.P + other.P),diploid_k)
        return zygote
    
    # make this work for odd numbers... like 45...    
    def set_ploidy(self,new_p):
        """only diploid to polyploid"""
        new_k = self.K*(new_p/self.P)
        
        
    def fitness(self,s,h=0.5):
        """"""
        w = 1 - s*(sum((self.K**(-1*np.log2(h)))))
        return w
        
        
class Ciliate:
    """"""
    def __init__(self,L):
        """"""
        self.germline = Genome(L,2)
        self.somatic = Genome(L,45)
        
    def mutate(self,mu):
        """"""
        self.germline.mutate(mu)
        self.somatic.mutate(mu)
    
    def asexual(self):
        """"""
        new_soma = self.somatic.amitosis()
        new_germ = self.germline.mitosis()
        daughter = Ciliate(self.germline.L)
        daughter.germline = new_germ
        daughter.somatic = new_soma
        return daughter
        
    def sex(self,other):
        """"""
        