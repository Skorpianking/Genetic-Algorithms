# Third GA program

import math
import random

# Taking a look at the Knapsack Problem (NP-Complete/NP-Hard) using a
# GA to try and find a solution. GA doesn't guarentee optimal solutions
# but it's another practive problem that isn't trivial by nature.

# Class for items placed in the knapsack.  With this class we could ask the
# question: what set of processes could a computer implement given a time
# constraint that will have the most value for a user.  Value obviously being
# already assigned to each process.
class Process:
    value = 0.00
    time = 0.00

    def __init__(self,x,y):
        self.value = x
        self.time = y

    def __repr__(self):
        return 'Value: ' + str(self.value) + ' Time: ' + str(self.time)


# Chromosome class
class Chromosome:
    name = ""
    fitness = 0.00

    def __init__(self):
        name = "0000000" # lenght of 7
        fitness = 0

    def __repr__(self):
        return 'Name: ' + self.name + ' Fitness: ' + str(self.fitness)

# First we will create items for the knapsack (2^7 solutions)
# value = 1st number, time = second number (ie weight)
dict = {
    0: Process(7,3),
    1: Process(9,4),
    2: Process(5,2),
    3: Process(12,6),
    4: Process(14,7),
    5: Process(6,3),
    6: Process(12,5)
    }

# A chromosome will be of the following form (0-1 knapsack problem)
# a b c d e f g
# 0 1 0 1 0 0 1 -- meaning its solution is b, d, and g (1 of each item)

# See: http://www.micsymposium.org/mics_2004/Hristake.pdf for further details
# on other ways to implement the population. I will stick to my normal
# 1-d array method

initialWeight = 22 # time limit / weight limit
population = [] # current population
length = 7 # size of chromosome (sticking with 0 = no, 1 = out, so max, 1 of each
pop_size = 10 # number of chromosomes to create/keep post breeding
mutation_rate = .001
xover_point = 4 # where we crossover values
numGens = 100 # number of generations we want to go through to find a solution
random.seed() # helps generate random chromosomes
sol = Chromosome() # best solution thus far

# Creates a random population of chromosomes
def createPopulation():
    for j in range(0, pop_size):
        val = ""
        for i in range(0,length):
            if random.random() > random.random():
                val = val + '1'
            else:
                val = val + '0'
        c = Chromosome()
        c.name = val
        population.append(c)

# Tests the population, assigns fitness value
def testPopulation():
    for item in population:
        fitness(item)

# Fitness function -- calculates the fitness of a chromosome.  In this
# problem, if the sum of the items exceeds the given weight bound, the
# fitness is assigned as 0.  Otherwise, it's fitness equals the total
# value of all the items placed in the knapsack.
def fitness(chrome):
    val = decode(chrome) # get the weight of this configuration
    if val > initialWeight:
        chrome.fitness = 0
    else:
        chrome.fitness = retVal(chrome)
        if chrome.fitness > sol.fitness:
            sol.fitness = chrome.fitness
            sol.name = chrome.name

# Decodes the current chromosome string and returns its weight
def decode(chrome):
    val = 0
    for i in range(0,length):
        if chrome.name[i]  == '1':
            val = val + dict.get(i).time
    return val

# Similar to decode, but this time, return the total value
def retVal(chrome):
    val = 0
    for i in range(0, length):
        if chrome.name[i] == '1':
            val = val + dict.get(i).value
    return val

# Build next generation.
def buildNewPopulation():
    newPop = []
    # Roulette wheel selection first (those with higher fitness scores have a better chance of
    # being selected for breeding)
    total_sum = sumPop() # sum the total value of the population's fitness scores
    # Build new population
    while len(newPop) != pop_size: 
        r = random.uniform(0, total_sum) # Get random number within this range
        a = findChrom(r) # find a chromosome in the population with fitness >= r
        r = random.uniform(0, total_sum) # Get random number within this range
        b = findChrom(r) # find a chromosome in the population with fitness >= r
        c = crossOver(a,b) # crossover the selected parents
        mutate(c); # add in possible mutation
        newPop.append(c) # add to the new population
    return newPop # next generation gets a chance to shine


# Mutates the chromosome with a set probability (steps through each bit, flips it if a threshold is met)
def mutate(chrome):
    for i in range(0, len(chrome.name)):
        if random.random() <= mutation_rate: # if met, flip this bit
            if chrome.name[i] == '1':
                chrome.name[i] == '0'
            else:
                chrome.name[i] == '1'

# Crosses the parents at a random point to create a child
def crossOver(a, b):
    # now cross at this point
    child = Chromosome()
    for i in range(0,xover_point):
        child.name = child.name + a.name[i]
    for i in range(xover_point, len(b.name)):
        child.name = child.name + b.name[i]
    return child

# Finds a chromosome in the population whose fitness is >= the number passed in
def findChrom(r):
    for item in population:
        if item.fitness >= r:
            return item
    # if none found, return a random element
    newR =  random.randint(0,pop_size-1)
    return population[newR]


# Sums fitness values of total population
def sumPop():
    total_sum = 0
    for item in population:
        total_sum = total_sum + item.fitness
    return total_sum
  
def main():
    print(dict)
    createPopulation()
    generation = 0
    while generation <numGens:
        testPopulation()
        population = buildNewPopulation()
        generation = generation + 1
    print('Generations calculated: ' + str(generation) + '!')
    print('Weight not exceeded: ' + str(initialWeight))
    print(sol.name)
    print('Time/Weight: ' + str(decode(sol)))
    print('Value: ' + str(sol.fitness))

main()
