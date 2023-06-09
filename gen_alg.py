import string
import random
import math
import os
import textwrap

bg_magenta = '\033[45m'
bg_cyan = '\033[46m'
bg_reset = '\033[0m'  # Reset to default background color

# DEFAULT ALGRORITHM PARAMETERS
STRING_LENGTH = 50          #length of target string
N_GENERATIONS = 200         #number of generations
N_SOL_PER_GEN = 15000       #number of solutions generated in a generation
MUTATION_RATE = 0.05        #need to check here
ELITSM = 0.06               #% of selections that move to next generation unaltered

string_length = STRING_LENGTH
n_generations = N_GENERATIONS
n_sol_per_gen = N_SOL_PER_GEN
mutation_rate = MUTATION_RATE    
elitism = ELITSM

#assign internal variables (allow user adjust parameters)
def reset_default_values():
    global string_length
    global string_length 
    global n_generations 
    global n_sol_per_gen 
    global mutation_rate  
    global elitism 

    string_length = STRING_LENGTH
    n_generations = N_GENERATIONS
    n_sol_per_gen = N_SOL_PER_GEN
    mutation_rate = MUTATION_RATE    
    elitism = ELITSM
    return 0           

def clear_screen(): #clear screen function 
    if os.name == 'posix':  # For Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')

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

def check_input():
    global string_length
    global string_length 
    global n_generations 
    global n_sol_per_gen 
    global mutation_rate  
    global elitism 
    
    clear_screen()
    input_text = """\
    MENU - Available commands:
    'adjust': see and update algorithm parameters
    'about' : explanation about this program
    Press ENTER just to skip:"""
    command = input(textwrap.dedent(input_text))
    if command == 'adjust':
        input_text = f"""\
        Enter number for choosing, current values are:
        1. String length: {string_length}
        2. N° of generations: {n_generations}
        3. N° solutions per generation: {n_sol_per_gen}
        4. Mutation rate: {mutation_rate}
        5. Elitism: {elitism}
        6. Reset to DEFAULT values
        Press ENTER just to skip:"""
        clear_screen()
        cmd = input(textwrap.dedent(input_text))
        if cmd == "1":
            string_length = int(input("Enter new value for string length:"))
        elif cmd == "2":
            n_generations = int(input("Enter new value for number of generations:"))
        elif cmd == "3":
            n_sol_per_gen = int(input("Enter new value for number of solutions per generation:"))
        elif cmd == "4":
            mutation_rate = float(input("Enter new value for mutation rate:"))
        elif cmd == "5":
            elitism = float(input("Enter new value for elitism rate:"))
        elif cmd == "6":
            reset_default_values()
    elif command == "about":
        print("Genetic algorithm implementation by Hernan G. 2023")
        input("Press ENTER just to continue:")

def exe_alg(target):

    global string_length
    global string_length 
    global n_generations 
    global n_sol_per_gen 
    global mutation_rate  
    global elitism

    nchar = len(target)
    #adjust target in case of more / less cgaracters than expected
    if nchar > string_length and nchar > STRING_LENGTH:      #truncate
        target = target[:string_length]
    elif nchar > string_length and nchar <= STRING_LENGTH:
        string_length = nchar   #adapt target
    elif len(target)<string_length:
        string_length = nchar     #reduce the space of soluctions if the string is shorter than expedted


    #calculate worst possible fitness value for the number of characters
    worst_fitness = fitness(' ','z') * string_length

    solutions_gen = gen_pool()  #create first generation of solutions 

    g = 0 # set numer of generation to zero

    exit = 0  #flag variable to exit the generation

    best = '' #control variable to check if adaptation approach is needed

    mutation_rate = MUTATION_RATE

    while (g < n_generations) and (exit == 0):

        candidates_next_gen = []
        mating_pool = []

        sel_mut = 0  #flag for controlling the selective mutation

        #test every solution and create mating pool
        for curr_sol in solutions_gen:
      
            curr_fit = fitness (target , curr_sol)            #determine the fitness of random generated solution

            if (curr_fit == 0):                               #if a solution is found, exit the loop
                exit = 1
            elif(curr_fit < 5):
                sel_mut = 1          #close to best solution, activate selective mutation

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

        if sel_mut == 1: #apply selective mutations on elite members
            for i in range(string_length):
                aux_str = list(next_gen[0]) 
                target_char = aux_str[i]
                char_upd = chr(ord(target_char)+1)               
                aux_str[i] = char_upd
                next_gen.append(''.join(aux_str))
                char_upd = chr(ord(target_char)-1)               
                aux_str[i] = char_upd
                next_gen.append(''.join(aux_str))


        for i in range(n_sol_per_gen-n_elite_members):     #mating process, mixing solution members
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)

            child = cross_over(parent1, parent2)            #mix parents and create new member solution

            for c in child:
                if random.random() < mutation_rate:
                    c = random.choice(string.ascii_lowercase+" ") #mutations by mutation rate

            next_gen.append(child)

        solutions_gen = next_gen

        clear_screen()
        print(f'Offspring generation N°{g+1} (sample):')   #for every generation print the best 10 solutions
        for i in range(10):
            if i == 0 and exit == 1:
                print(bg_cyan + next_gen[i] + ' * FOUND :) *' + bg_reset )
            elif i==0 and exit == 0:
                print(bg_magenta + next_gen[i] + ' * CLOSEST BEST FOUND :! *' + bg_reset )
                #if no progress, auto adapt mutation rate --> expands the space of solutions 
                if best == next_gen[i]:
                    if mutation_rate <=0.9:
                        mutation_rate = mutation_rate * 1.1      
                best = next_gen[i]
            else:
                print(next_gen[i])
        


        g +=1 # move to next generation

    mutation_rate = MUTATION_RATE

    input('Press ENTER')
    clear_screen()

#main program 
clear_screen()
command = 'x'
while command != 'exit':
    input_text = f"""\
    Enter a target string (Max. nr. of characters {STRING_LENGTH} and lowercase) 
    or 'menu' for more options
    or 'exit' to quit the program
    Your target string:"""
    command = input(textwrap.dedent(input_text))
    if command == 'menu':
        check_input()
    elif command != '' and command != 'exit':
        exe_alg(command)
    clear_screen()

#end main program





