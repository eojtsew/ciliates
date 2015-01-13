#!/usr/bin/python
"""
Created on Fri Sep  6 03:50:32 2013

@author: joe
"""

    def assorted(self,locus):
        """"""
        unique = []
        for i in range(len(locus)):
            if locus[i] not in unique:
                unique.append(locus[i])
        if len(unique) > 1:
            return False
        else:
            return True
                
    def is_assorted(self):
        """"""
        assorted_ls = []
        for i in range(self.L):
            assorted_ls.append(self.assorted(self.somatic[:,i]))
        return assorted_ls
        
    def all_assorted(self):
        """"""
        assort_ls = self.is_assorted()
        assort_count = np.sum(assort_ls)
        print assort_count
        if assort_count < self.L:
            return False
        if assort_count == self.L:
            return True
            
    def run_assortment(self):
        """"""
        count = 0
        all_assort = self.all_assorted()
        while not all_assort:
            self = self.reproduce()
            count += 1
            all_assort = self.all_assorted()
        return count
        
    def mutate_germline(self,mu,values):
        """Mutates each allele at each locus in the germline to the given value
        with probability mu. Uses numpy.random.binomial to determine which
        alleles mutate, then uses a boolean array to assign the value those
        alleles. Right now, mutations are irreversible...
        (currently using value = 0 for wild-type, value = -1 for deleterious
        mutations, and value = 1 for beneficial mutations)."""
        mutants = (np.random.binomial(1,mu,(2,self.L)) == 1) & (self.germline == 0)
        self.germline[mutants] = values
        
    def mutate_somatic(self,mu,values):
        """Mutates each allele at each locus in the somatic to the given value
        with probability mu. Uses numpy.random.binomial to determine which
        alleles mutate, then uses a boolean array to assign the value those
        alleles. Right now, mutations are irreversible...
        (currently using value = 0 for wild-type, value = -1 for deleterious
        mutations, and value = 1 for beneficial mutations)."""
        mutants = (np.random.binomial(1,mu,(45,self.L)) == 1) & (self.somatic == 0)
        self.somatic[mutants] = values
        
    def fitness_old(self,s,h):
        # Doesn't work for new mutate method...
        """Calculates additive fitness..."""
        deleterious = (self.somatic == -1)
        beneficial = (self.somatic == 1)
        d = sum((np.mean(deleterious,axis=0)**(np.log(h)/np.log(0.5)))*s)
        b = sum((np.mean(beneficial,axis=0)**(np.log(h)/np.log(0.5)))*s)
        w = 1 - d + b
        return w
        
        
        
        
        
        