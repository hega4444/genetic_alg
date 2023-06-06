import string
import random
import math

# DEFAULT PARAMETERS
STRING_LENGTH = 20          #length of target string
N_GENERATIONS = 100         #number of generations
N_SOL_PER_GEN = 1000        #number of solutions generated in a generation
MUTATION_RATE = 0.01        #need to check here
ELITSM = 0.05               #% of selections that move to next generation unaltered


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

def cross_over(parentA, parentB): #funtion to create a child string from two parent strings
    midPoint = random.randint(0,len(parentA))   #select an arbitrary middle point
    child = parentA[0:midPoint] + parentB[midPoint:len(parentA)]
    return child

def gen_pool():
    pool_sol = []
    for i in range(n_sol_per_gen):
        sol = gen_random_string(string_length)       #create first generation of solutions
        pool_sol.append(sol)
    return pool_sol


#begin of main program

target = input(f'Enter a target string (Max. nr. of characters {string_length} and lowercase):')
#adjust target in case of more / less cgaracters than expected
if len(target)>string_length:      #truncate
    target = target[:string_length]
elif len(target)<string_length:
    target = target + ''.join(' ' for i in range(string_length-len(target)))  #fill with spaces


#calculate worst possible fitness value for the number of characters
worst_fitness = fitness(' ','z') * string_length

solutions_gen = gen_pool()  #create first generation of solutions 

for g in range(n_generations):

    candidates_next_gen = []
    mating_pool = []

    #test every solution and create mating pool
    for curr_sol in solutions_gen:

        curr_fit = fitness (target , curr_sol)            #determine the fitness of random generated solution

        mating_chances = math.floor((worst_fitness-curr_fit) * 100 / worst_fitness)  #calculate mating chances

        gen_tuple = (curr_sol, curr_fit, mating_chances)
        
        candidates_next_gen.append(gen_tuple)                 #append solution to list

        for n in range(mating_chances):
            mating_pool.append(curr_sol)       #add member n times to increase chances in mating lottery


    candidates_next_gen.sort(key=lambda x: x[1])      #sort solutions by their fitness function

    n_elite_members = math.floor(n_sol_per_gen*elitism) #calculate number of elite members

    next_gen = []

    for i in range(n_elite_members):           #include in the next generation a number of members without altering
        next_gen.append(candidates_next_gen[i][0])

    for i in range(n_sol_per_gen-n_elite_members):     #mating process, mixing solution members
        parent1 = random.choice(mating_pool)
        parent2 = random.choice(mating_pool)

        child = cross_over(parent1, parent2)            #mix parents and create new member solution
        next_gen.append(child)

    solutions_gen = next_gen

    print(f'Offspring generation N°{g+1} (sample):')
    for i in range(10):
        print(next_gen[i])
    






