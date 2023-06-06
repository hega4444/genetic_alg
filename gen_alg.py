import string
import random
import math

# DEFAULT PARAMETERS
STRING_LENGTH = 4           #length of target string
N_GENERATIONS = 2           #number of generations
N_SOL_PER_GEN = 100         #number of solutions generated in a generation
MUTATION_RATE = 0.01        #need to check here
ELITSM = 0.1                #% of selections that move to next generation unaltered


#assign internal variables (allow user adjust parameters)
string_length = STRING_LENGTH
n_generations = N_GENERATIONS
n_sol_per_gen = N_SOL_PER_GEN
mutation_rate = MUTATION_RATE    
elitism = ELITSM           


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

target = input(f'Enter a target string (Max. nr. of characters {string_length} and lowercase):')
#adjust target in case of more / less cgaracters than expected
if len(target)>string_length:      #truncate
    target = target[:string_length]
elif len(target)<string_length:
    target = target + ''.join(' ' for i in range(string_length-len(target)))  #fill with spaces


#calculate worst possible fitness value for the number of characters
worst_fitness = fitness('a','z') * string_length

solutions_gen = [] #list for generated solutions

for i in range(n_sol_per_gen):
    curr_sol = gen_random_string(string_length)     #create first generation of solutions 
    curr_fit = fitness (target , curr_sol)          #determine the fitness of random generated solution

    gen_tuple = (curr_sol, curr_fit)                #create a tuple with solutuon and fitness function

    solutions_gen.append(gen_tuple)                 #append solution to list

    mating_chances = math.floor(curr_fit * 100 / worst_fitness)  #calculate mating chances




solutions_gen.sort(key=lambda x: x[1])      #sort solutions by their fitness function

for i in solutions_gen:
    print(i)





