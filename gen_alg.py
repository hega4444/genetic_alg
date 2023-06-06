import string
import random

#PARAMETERS
STRING_LENGTH = 4
N_GENERATIONS = 2
N_SOL_PER_GEN = 100     #number of solutions generated in a generation
MUTATION_RATE = 0.01    #need to check here
ELITISM = 0.1           #% of selections that move to next generation unaltered


def gen_random_string(length): #function to create random solutions
    #choose from all lowercase letter
    letters = string.ascii_lowercase   #coming from string module
    return ''.join(random.choice(letters+ " ") for i in range(length)) #including the space character in the possible choices

def fitness(goal, pos_solution): #function to evaluate fitness of a given solution 
    sum_error = 0
    for i in range(len(goal)):
        sum_error += abs(ord(goal[i])-ord(pos_solution[i]))
    return sum_error



#begin of main program

target = input(f'Enter a target string (Max. nr. of characters {STRING_LENGTH} and lowercase):')
#adjust target in case of more / less cgaracters than expected
if len(target)>STRING_LENGTH:      #truncate
    target = target[:STRING_LENGTH]
elif len(target)<STRING_LENGTH:
    target = target + ''.join(' ' for i in range(STRING_LENGTH-len(target)))  #fill with spaces


solutions_gen = [] #list for generated solutions

for i in range(N_SOL_PER_GEN):
    gen = gen_random_string(STRING_LENGTH)  #create first generation of solutions 
    fit = fitness (target , gen)            #determine the fitness of random generated solution

    gen_tuple = (gen, fit)                  #create a tuple with solutuon and fitness function

    solutions_gen.append(gen_tuple)         #append solution to list

solutions_gen.sort(key=lambda x: x[1])      #sort solutions by their fitness function

for i in solutions_gen:
    print(i)




