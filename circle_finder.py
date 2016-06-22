# Second GA program

import math
import random
from circle_class import Circle # import my circle class
from tkinter import*

# Problem found @ AI-junkie.com. This file uses a GA to find the largest circle that can fill a
# space between other circles in the given grid.  All that is necessary for the other circles
# are their origins and radii.

# A circle class is provided to speed comparisons needed by the fitness function.  Fitness is
# based on area if a circle doesn't intersect others.  Future improements could be made by
# allowing floating points for x/y/radius (may allow tighter fits), as well as possibly
# developing a fitness that allows intersections as possible answers, assigning a fitness with
# a penalty.  For now, Occum's Razor, intetsecting circles or circles containing others will
# be assigned a fitness of 0.


# In this implementation, we will have three locii.  The first will represent the X coord,
# the second the Y coord, and finally, the third is the radius.  We are allowing binary values
# that translate from (0-500) in base 10.  This means each locus is of length 9.
class Chromosome:
    name = ""
    fitness = 0.00

    def __init__(self):
        self.name = "000000000000000000000000000" # max value of 500
        self.fitness = 0.00

    def __repr__(self):
        return 'Name: ' + self.name + ' Fitness: ' + str(self.fitness)

# World variables
sol = Chromosome() # best solution found so far
population = [] # current population 
random.seed() # help generate random chromosomes
length = 27 # chromosome length
pop_size = 100 # must(?) be divisible by 4
mutation_rate = .001 # likelihood of mutation
xover_point = 18 # point of crossover for parent pairs (will change radius)
numGens = 100 # number of generations we wish to iterate through

# TK World Variables
master = Tk()
canvas_width = 500
canvas_height = 500

# No dictionary necessary for conversion, we will simply translate from a 10 digit bin to decimal
# accomplished via int(<10 digit str>, base=2), will convert the string to a base 10 number

# Initial list of circles.  Keeping it small at the moment since the fitness function will
# compare a population of M circles by the number N circles here.  This can result in a
# O(n^2) operation -- plus we do this for P number of generations O(n^3)
initial_list = [ Circle(100,150,65), Circle(200,300, 105), Circle(450,150,50),
                 Circle(200,50,10), Circle(300,50,30), Circle(400,400,25),
                 Circle(400,300,25) ]


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

# Decodes the name of a chromosome into its 3 locii (also does base2 to 10 conversion)
def decode(chrome):
    val = ""
    for i in range(0, length, 9):
        val = val + str(int(chrome.name[i:i+9], base=2)) + ' '
    #print(val)
    return val

# Test each member of the population
def testPopulation():
    for item in population:
        fitness(item)

# Fitness function -- we will test the random circle against circles in the initial list.
# Only if it doesn't intersect or contain(s) other circles, will fitness be assigned
# Fitness will equal its area.
def fitness(chrome):
    val = decode(chrome) # interpret the circle
    xyrad = val.split()
    circ = Circle(int(xyrad[0]),int(xyrad[1]), int(xyrad[2]))
    # Evaluate this circle against all the circles in the initial_list
    # Also do a bounds check for drawing the circle on the screen
    for item in initial_list:
        if circ.intersects(item) == True:
            return
        if circ.containsCircle(item) == True:
            return
        if circ.x  + circ.radius > canvas_width or circ.x - circ.radius < 0:
            return
        if circ.y + circ.radius > canvas_height or circ.y - circ.radius < 0:
            return
    chrome.fitness = circ.area()
    if chrome.fitness >= sol.fitness:
        sol.fitness = chrome.fitness
        sol.name = chrome.name


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


# Functions to TK
def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")

def circle(canvas,x,y, r):
   id = canvas.create_oval(x-r,y-r,x+r,y+r)
   return id


# main function
def main():
    
    createPopulation()
    generation = 0
    while generation <numGens:
        testPopulation()
        population = buildNewPopulation()
        generation = generation + 1
    print(sol.name)
    print('Generations calculated: ' + str(generation) + '!')
    print(str(decode(sol)))
    print(str(sol.fitness))
    xyrad = decode(sol).split()
    x = int(xyrad[0])
    y = int(xyrad[1])
    r = int(xyrad[2])

    circ = Circle(x,y,r)
    

    w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
    w.pack()

    checkered(w,20)

    # following circles are "static" and will be added to the finder program

    circle(w, 100, 150, 65)
    circle(w, 200, 300, 105)
    circle(w, 450, 150, 50)
    circle(w, 200, 50, 10)
    circle(w, 300, 50, 30)
    circle(w, 400, 400, 25)
    circle(w, 400, 300, 25)

    w.create_oval(x-r,y-r,x+r,y+r, fill="green") # new circle   

    mainloop()


    
    
# run the program
main()
    
