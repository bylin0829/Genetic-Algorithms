# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:33:07 2017

@author: bylin
"""
from numpy.random import randint, uniform, random
from time import sleep
# import numpy as np

""" 
find minimum, mode = 0
find maximum, mode = 1
"""

class GeneticAlgorithms:
    def __init__(self, MODE=1, POPULATION_SIZE=40, PROB_CROSSOVER=0.9, PROB_MUTATION=0.1, TERMINATION=500, LOWER_BOUNDARY=-2, UPPER_BOUNDARY=20):
        self.mode=MODE
        self.groupsize=POPULATION_SIZE # population size
        self.pc=PROB_CROSSOVER # probability of performing crossover, 0.9 = 90%
        self.pm=PROB_MUTATION # pm, probability of mutation, 0.1 = 10%
        self.termination=TERMINATION # if best value keep "interval" times, stop this program
        self.lower_boundary=LOWER_BOUNDARY
        self.upper_boundary=UPPER_BOUNDARY

        if self.lower_boundary > self.upper_boundary:
            raise ValueError('The lower_boundary greater than upper_boundary!')
        if self.termination <= 0:
            raise ValueError('The termination is less than or equal to zero!')
    
    # input function
    def fitness(self, x):
        return (x+7)**2

    def selection(self, chromosome):
        group = []
        mother = []
        fnval = []
        
        # calculate fitness 
        for i in range(self.groupsize):
            if self.mode == 0:
                # find minimum
                fnval.append(1/self.fitness(chromosome[i]))
            else:
                # find maximum
                fnval.append(self.fitness(chromosome[i]))
        
        # Copy the best chromosomes for selection
        for i in range(self.groupsize):
            iscopy = round(self.groupsize*fnval[i]/sum(fnval))
            if iscopy:
                group.append(chromosome[i])

        # Roulette Wheel Selection
        while len(mother) < self.groupsize:
            mother.append(group[int(randint(0,len(group)-1))])
        return mother

    def crossover(self, parents):
        next_generation = []
        while len(next_generation) < self.groupsize:
            mother_index = randint(0,self.groupsize)
            father_index = randint(0,self.groupsize)
            # Avoid the same parents
            while mother_index == father_index:
                father_index = randint(0,self.groupsize)
            mother = parents[mother_index]
            father = parents[father_index]

            if random() < self.pc:
                # Interpolation
                child1 = (mother+father)/2
                child2 = child1
            else:
                child1 = mother
                child2 = father
            next_generation.append(child1)
            next_generation.append(child2)
        return next_generation

    def mutation(self, group):
        for a in range(len(group)):
            if(random() < self.pm):
                # Activation mutation
                group[a] = uniform(self.lower_boundary, self.upper_boundary)
        return group
        
    def best_result(self, generation):
        fit=[]
        for a in range(self.groupsize):
            if self.mode == 0:
                ### find minimum ###
                fit.append(1/self.fitness(generation[a]))
            else:
                ### find maximum ###
                fit.append(self.fitness(generation[a]))
            
        tt = fit.index(max(fit))
        best_chromo = generation[tt]
        return best_chromo
    
    def start(self):
        # Initialize
        result = 0
        generation_count = 0
        termination_count = 0

        # Generate the first group
        group = (uniform(self.lower_boundary, self.upper_boundary, self.groupsize))
        # Start GA
        while generation_count < self.termination:
            group = self.selection(group)
            group = self.crossover(group)
            group = self.mutation(group)
            result = self.best_result(group)
            # print(result)
            generation_count += 1
            # sleep(0.1)
        if termination_count >= self.termination:
            print('Stop by best value keep on {generation} generation'.format(generation=self.termination))
        print('Last generation = {generation_count}'.format(generation_count=generation_count))

        return result

if __name__ == '__main__':
    mytest = GeneticAlgorithms()
    result = mytest.start()
    print('Best value = {result:.2f}'.format(result=result))