# First attempt at Genetic Algorithms

import random

# This file uses a GA to find an answer to a given input number.
# Given the digits 0 through 9 and the operators +, -, * and /,  find a sequence that will represent
# a given target number.
# The operators will be applied sequentially from left to right as you read.
# So, given the target number 17, the sequence 6+5*4/2+1 would be one possible solution. Order of ops is
# enforced because the python eval() function rocks like that.

# Refined a couple of items to try and get better performance.  For example, instead of a completely random
# string of 1's and 0's, it builds a chromosome of the form num op num op ... num, where each piece
# is selected randomly from the dictionary of known good values.  This improvement seemed to help the
# algorithm converge in the general area of a solution more often.  I also modified the crossover area
# to happen at the 16th place (num op num op XXXX XXXX XXXX ....).  I didn't notice a huge improvement
# in the algorithm. 

# Define class Chromosome
class Chromosome:
    name = ""
    fitness = 0.00
    expression = ""

    def __init__(self):
        self.name = ""
        self.fitness = 0.00
        self.expression = ""
    

# Build dictionary
dict = { '0000': 0,
         '0001': 1,
         '0010': 2,
         '0011': 3,
         '0100': 4,
         '0101': 5,
         '0110': 6,
         '0111': 7,
         '1000': 8,
         '1001': 9,
         '1010': '*',
         '1011': '/',
         '1100': '+',
         '1101': '-' }

numList = ['1','2','3','4','5','6','7','8','9','0']
opList = ['*', '/', '-', '+']


# world variables
sol = Chromosome() # solution
currChrom = "" # current chromosome being tested
population = [] # list of chromosomes
random.seed() # helps us generate random chromosomes

# world variables that affect the GA's performance and values it can find
length = 36 # chromosome length
pop_size = 50 # population size -- must be divisible by 4
mutation_rate = .001 # can increase/decrease likelihood of mutation here


# Will create a random population of pop_size of chromosomes, each of length 'length'
def createPopulation():
    #print('Creating Initial Population!')
    # automatically creating a string of size 'length' then flipping 'bits' as we go
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


#    for j in range(0, pop_size):
#        val = ""
#        q = True 
#        for i in range(0,length,4):
#            k = random.randint(0,10)
#            if k == 0 and q == True:
#                val = val + '0000'
#                q = False
#            elif k == 1 and q == True:
#                val = val + '0001'
#                q = False
#            elif k == 2 and q == True:
#                val = val + '0010'
#                q = False
#            elif k == 3 and q == True:
#                val = val + '0011'
#                q = False
#            elif k == 4 and q == True:
#                val = val + '0100'
#                q = False
#            elif k == 5 and q == True:
#                val = val + '0101'
#                q = False
#            elif k == 6 and q == True:
#                val = val + '0110'
#                q = False
#            elif k == 7 and q == True:
#                val = val + '0111'
#                q = False
#            elif k == 8 and q == True:
#                val = val + '1000'
#                q = False
#            elif k == 9 and q == True:
#                val = val + '1001'
#                q = False
#            else:
#                k = random.randint(0,4)
#                if k == 0:
#                    val = val + '1010'
#                elif k == 1:
#                    val = val + '1011'
#                elif k == 2:
#                    val = val + '1100'
#                else:
#                    val = val + '1101'
#                q = True
#        c = Chromosome()
#        c.name = val
#        population.append(c)
            

# Decodes a chromosome into an expression
def decode(chrome):
    val = ""
    for i in range(0,length,4):
        if dict.get(chrome[i:i+4]) != None:
            val = val + str((dict.get(chrome[i:i+4])))
        else:
            val = val + 'E' # E stands for empty, it allows us to quickly ignore 'bad' parts of a chromosome
    return val
                
    
# Tests each member of the population for fitness
def testPopulation(value):
    #print('Testing the Population!')
    for item in population:
        fitness(item, value) # decodes the chromosome and assigns its fitness score

# Fitness -- fitness score = 1 / (user number - decoded number), div by zero is and exact answer
# may build a "close" enough value later on
def fitness(chrome, value):
    val = decode(chrome.name)
    newVal = buildExpress(val) # parse into an expression that may be evaluated
    chrome.expression = newVal
    num = 0
    # if final value is unparsable, then fitness value becomes 0
    try:
        num = eval(newVal)
    except AttributeError:
        num = 0
    except NameError:
        num = 0
    except SyntaxError:
        num = 0
    except ZeroDivisionError:
        num = 0

    # see if we have a solution
    try:
        num = 1 / (int(value)- num)
    except ZeroDivisionError:
        sol.fitness = 100
        sol.name = chrome.name
        sol.expression = chrome.expression
        print('Solution found')
    else:
        chrome.fitness = abs(num) # overestimating is ok, it gets us close to the solution we want
        if chrome.fitness > sol.fitness : # <-------- experimenting
            sol.name = chrome.name
            sol.fitness = chrome.fitness
            sol.expresion = chrome.expression

# Parses decoded chromosome expression into, hopefully, one that can be evaluated
def buildExpress(val):
    # Go through the string to build a math expression Python can actually parse
    # As we go through, we keep values if inline with the expression
    # For example, 2 2 + E - 7 2, becomes 2 + 7, keeping the first encountered
    # number, then an operator, then number and so on
    numFlag = 0 # basically booleans to keep us straight 
    opFlag = 0
    newVal = "" # expression we are building
    for i in range(0, len(val)):
        #print(val[i])
        if val[i] in numList and numFlag == 0 and opFlag == 0: # found first number, no operators
            newVal = newVal + val[i]
            numFlag = 1
        elif val[i] in opList and numFlag == 1 and opFlag == 0: # found first operator after number
            newVal = newVal + val[i]
            opFlag = 1
        elif val[i] in numList and numFlag == 1 and opFlag == 1: # found second number (post operator)
            newVal = newVal + val[i]
            opFlag = 0
    # because it's late at night and I don't want to mess with it, just check the last value
    # in the new string, if it's in the opList, remove it from the string
    if newVal[len(newVal)-1] in opList:
        newVal = newVal[:-1] # remove this last character
    return newVal


# Builds the next generation of chromosomes to test on. It selects a parent pair from the
# current population to produce an offspring.  After crossover, there is a small mutation
# chance.  Then offspring is added to the new population pool.
def buildNewPopulation():
    #print('Building New Population!')
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
    for i in range(0, len(chrome.name), 4):
        if random.random() <= mutation_rate: # if met, flip this bit
            if chrome.name[i] == '1':
                chrome.name[i] == '0'
            else:
                chrome.name[i] == '1'

# Crosses the parents at a random point to create a child
def crossOver(a, b):
 #   rand = random.randint(0, length)
    # now cross at this point
    child = Chromosome()
    for i in range(0,16):
        child.name = child.name + a.name[i]
    for i in range(16, len(b.name)):
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

# Runs until solution is found -- or a set number of generations is produced
def geneticSearch(value):
    print('Beginning my search for an expression that equals: ' + str(value))
    createPopulation()
    generation = 0
    while sol.fitness != 100 and generation < 1000:
        testPopulation(value)
        if sol.fitness != 100:
            population = buildNewPopulation()
        generation = generation + 1
    print('Generations calculated: ' + str(generation) + '!')
    

def main():
    value = input('Enter a number to find expression for: ') # Get user input
    geneticSearch(value) # Begin GA search
    print(sol.fitness) 
    print(sol.name)
    print(buildExpress(decode(sol.name)))
    print(eval(buildExpress(decode(sol.name)))) # Return solution, or closest found

# run main from this file
main()
