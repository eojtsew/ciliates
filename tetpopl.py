#!/usr/bin/python
"""
Created on Fri Aug  9 00:15:19 2013
@author: joe
"""

from newTet import *
import numpy as np

class Population:
    """"""
    def __init__(self,N,L=200,tet_germ=None,s_b=0.02,s_d=-0.02,beta_b=1,beta_d=1,mu_b_germ=0.01,mu_d_germ=0.02,mu_b_soma=0.01,mu_d_soma=0.02):
        """"""
        self.N = N
        self.L = L
        self.generation = 0
        self.s_b = s_b
        self.s_d = s_d
        self.beta_b = beta_b
        self.beta_d = beta_d
        self.mu_b_germ = mu_b_germ
        self.mu_d_germ = mu_d_germ
        self.mu_b_soma = mu_b_soma
        self.mu_d_soma = mu_d_soma
        self.orgs = []
        if tet_germ != None:
            for i in range(self.N):
                self.orgs.append(Tet(self.L,tet_germ))
        else:
            for i in range(self.N):
                self.orgs.append(Tet(self.L))
        self.orgs = np.array(self.orgs)
        
    def set_orgs(self,orgarr):
        """"""
        self.orgs = orgarr
        return
        
    def __repr__(self):
        return str(self.orgs)
        
    def mutations(self):
        """probs a faster way to do it..."""
        for i in range(self.N):
            self.orgs[i].mutate(self.mu_b_germ,self.s_b,self.beta_b,'germline')
            self.orgs[i].mutate(self.mu_d_germ,self.s_d,self.beta_d,'germline')
            self.orgs[i].mutate(self.mu_b_soma,self.s_b,self.beta_b,'somatic')
            self.orgs[i].mutate(self.mu_d_soma,self.s_d,self.beta_d,'somatic')
                
    def get_fitnesses(self,how="mult"):
        """probs a faster way to do it..."""
        w = []
        for i in range(self.N):
            self.orgs[i].set_fitness(how)
            w.append(self.orgs[i].fitness)
        return np.array(w)            
            
    def reproduction(self):
        #this seems overly simplistic...
        """Applies Tet.reproduce() to each member of the population."""
        for i in range(self.N):
            self.orgs[i] = self.orgs[i].reproduce()
        self.generation += 1
        
    #def next_generation_old(self):
        #""""""
        #self.mutations()
        #self.reproduction()
        #w = self.get_fitnesses()
        #relative_w = []
        #for i in range(self.N):
            #relative_w.append(w[i]/sum(w))
        #new = np.random.choice(range(self.N),self.N,replace=True,p=relative_w)
        #self.orgs = new
        #self.generation += 1

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
            
class Evolve:
    """"""
    def __init__(self,population,generations=200):
        """"""
        self.population = population
        self.tot_gens = generations
        self.data = []
        self.all_pops = []
        
    def run_it(self):
        """"""
        while self.population.generation < self.tot_gens:
            self.data.append(self.population.get_fitnesses())
            self.all_pops.append(self.population.orgs)
            self.population.next_generation()
            print np.mean(self.population.get_fitnesses())
        return self.population.fitnesses()
        

        
        

                
