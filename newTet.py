#!/usr/bin/python
"""
Created on Fri Jun 21 11:55:54 2013
@author: joe
"""

import numpy as np
from numpy.random import gamma
from numpy import inf

def mutational_effects(n, s, beta):
    """
    Generate n mutations from a gamma distribution with mean effect s and shape parameter beta.
    Negative (positive) values of s indicate deleterious (beneficial) mutations. 
    
    Arguments:
    n -- number of mutations
    s -- mean effect of a mutation
    beta -- shape parameter of the gamma distribution (inf indicates equal effects)
    """
    if np.sign(s) == 1:
        beneficial = True
    elif np.sign(s) == -1:
        beneficial = False
    else:
        return "Invalid s: must be nonzero."
    if beta > 0:
        if beta == inf:
            mutations = np.repeat(s, n)            
        else:
            alpha = beta / abs(s)
            if beneficial:
                mutations = gamma(shape=beta, scale=1/alpha, size=n)
            else:
                mutations = - gamma(shape=beta, scale=1/alpha, size=n)
        return mutations
    else:
        return "Invalid beta: must be 0 < beta < inf."

class Tet:
    """
    Represent individual organism.
    
    Attributes:
    L - Number of loci.
    germline - 2xL array representing the diploid germline genome.
    somatic - 45XL array representing the somatic genome.
    """
    def __init__(self, L=100, germline=None, somatic=None):
        """
        Initialize a Tet object.
        
        Arguments:
        L - Number of loci (default is 100).
        germline - An array with shape (2,L) or None (default is None).
            If germline argument is None, then a 2xL array of zeros.
        somatic - An array with shape (45,L) or None (default is None).
            If somatic argument is None, then a 45xL array of zeros.
        
        NOTE: Doesn't check germline/somatic type or shape. FIX.
        """
        self.L = L
        self.fitness = None
        self.somatic = np.zeros((45,self.L))
        if germline is None:
            self.germline = np.zeros((2,self.L))
            if somatic is None:
                self.somatic = np.zeros((45,self.L))
        else:
            self.germline = germline.copy()
            if somatic == None:
                self.somatic[0:23,:] = self.germline[0,:]
                self.somatic[23:,:] = self.germline[1,:]
            else:
                self.somatic = somatic.copy()
            
    def __repr__(self):
        """Return the string representation of each genome."""
        s = "Germline:\n" + str(self.germline) + "\nSomatic:\n" + str(self.somatic)
        return s
        
    def mutate(self,mu,s,beta,genome='both'):
        """"""
        if genome == 'somatic' or genome == 'both':
            mutants = (np.random.binomial(1,mu,(45,self.L)) == 1) & (self.somatic == 0)
            n = np.sum(mutants)
            effects = mutational_effects(n,s,beta)
            self.somatic[mutants] = effects
        if genome == 'germline' or genome == 'both':
            mutants = (np.random.binomial(1,mu,(2,self.L)) == 1) & (self.germline == 0)
            n = np.sum(mutants)
            effects = mutational_effects(n,s,beta)
            self.germline[mutants] = effects
        #self.set_fitness("add")
        
    def reproduce(self):
        """Returns a new Tet object. The germline genome of the new individual
        is copied from the progenater. To form the new somatic genome, the
        somatic genome of the progenater is duplicated and each locus is
        sampled without replacement 45 times using numpy.random.choice."""     
        dup_somatic = np.zeros((90,self.L))
        dup_somatic[:45] = self.somatic.copy()
        dup_somatic[45:] = self.somatic.copy()
        new_tet = Tet(self.L)
        for i in range(self.L):
            new_tet.somatic[:,i] = np.random.choice(dup_somatic[:,i],45,False)
        new_tet.germline = self.germline
        return new_tet

    def set_fitness(self,flavor="mult"):
        """flavors: mult for multiplicative, add for additive"""
        if flavor == "mult":
            self.mult_fitness()
        elif flavor == "add":
            self.add_fitness()
        else:
            return "must specify 'add' or 'mult'"
    
    def add_fitness(self):
        """supposed to be additive fitness... meh..."""
        w = sum(np.mean(self.somatic,axis=0))
        self.fitness = w
        #return w
        
    def mult_fitness(self):
        """multiplicative fitness"""
        w = np.prod(np.prod((self.somatic + 1),axis=0))
        self.fitness = w
        #return w
        
    def genomic_exclusion(self):
        """Generates a haploid genotype from the germline, then generates a
        full homozygote. The resulting individual can be used to assess the
        fitness of the germline."""
        homozyg_germ = self.ge_round_one()
        GE_tet = Tet(self.L,homozyg_germ)
        return GE_tet
        
    def ge_round_one(self):
        """Return a homozygous diploid germline genome (like round 1 of genomic exclusion...)"""
        which_allele = np.random.binomial(1,0.5,self.L) == 0
        hap_germ = np.where(which_allele,self.germline[0,:],self.germline[1,:])
        homozyg_germ = np.zeros((2,self.L))
        homozyg_germ[0:2,:] = hap_germ
        #GE_tet = Tet(self.L,homozyg_germ)
        #return GE_tet
        return homozyg_germ
        
    def sex(self,other):
        """Return one sexual offspring from the two specified Tet parents"""
        s_alleles = np.random.binomial(1,0.5,self.L) == 0
        s_germ = np.where(s_alleles,self.germline[0,:],self.germline[1,:])
        o_alleles = np.random.binomial(1,0.5,other.L) == 0
        o_germ = np.where(o_alleles,other.germline[0,:],other.germline[1,:])
        new_germ = np.zeros((2,self.L))
        new_germ[0,:] = s_germ
        new_germ[1,:] = o_germ
        new_soma = np.zeros((45,self.L))
        new_soma[0:23,:] = s_germ
        new_soma[23:45,:] = o_germ
        progeny = Tet(self.L, new_germ, new_soma)
        return progeny
        
