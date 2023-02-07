from gp_funcs import *
import matplotlib.pyplot as plt

"""
    (i) one-max problem (uses all the standard functions for fitness and mutation)
"""
def part_i():
    
    # setting the composition (what the string is made up of), target (e.g. target string or fitness score),
    # length of genomes, size of population
    composition = [0, 1]
    target = 1.0 # here we want the algorithm to reach a goal of top fitness, however this can be lowered to get lower fitness if the need arises
    length = 30
    size = 30

    # completing evolution using functions from the gp_funcs class found in the other file
    gp = gp_funcs(composition, target, length, size)
    end_population, iterations, avg_fitness_per_gen = gp.evolution(
        gp.pop_generation, gp.simple_fitness, 
        gp.selection_function, gp.one_point_crossover, 
        gp.standard_mutation
    )

    # printing info to terminal and generating plots for this part
    print_statistics(end_population, round(target, 1), iterations, "i")
    plot_avgf_vs_gens("Part (i)", iterations, avg_fitness_per_gen)


"""
    (ii) evolving to a target string (using a different fitness function)
"""
def part_ii():

    # setting the composition (what the string is made up of), target (e.g. target string or fitness score),
    # length of genomes, size of population
    composition = [0, 1]
    target = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0]
    length = 30 # make sure length is the same size as target if target string is set as goal
    size = 30

    # completing evolution using functions from the gp_funcs class found in the other file
    gp = gp_funcs(composition, target, length, size)
    end_population, iterations, avg_fitness_per_gen = gp.evolution(
        gp.pop_generation, gp.part2_fitness, 
        gp.selection_function, gp.one_point_crossover, 
        gp.standard_mutation
    )

    # printing info to terminal and generating plots for this part
    print_statistics(end_population, target, iterations, "ii")
    plot_avgf_vs_gens("Part (ii)", iterations, avg_fitness_per_gen)


"""
    (iii) deceptive landscape (using different fitness function)
"""
def part_iii():
    
    # setting the composition (what the string is made up of), target (e.g. target string or fitness score),
    # length of genomes, size of population
    composition = [0, 1]
    target = 1.0 # however if all 0's we will get 2.0 as our fitness score for that one solution which will also end the evolution (acts like an easter egg)
    length = 30 # make sure length is the same size as target if target string is set as goal
    size = 30

    # completing evolution using functions from the gp_funcs class found in the other file
    gp = gp_funcs(composition, target, length, size)
    end_population, iterations, avg_fitness_per_gen = gp.evolution(
        gp.pop_generation, gp.part3_fitness, 
        gp.selection_function, gp.one_point_crossover, 
        gp.standard_mutation    # , test_part3 = True # this allows for testing fitness function for part 3
    )

    # printing info to terminal and generating plots for this part
    print_statistics(end_population, round(target, 1), iterations, "iii", ", or '2.0' if all were 0's")
    plot_avgf_vs_gens("Part (iii)", iterations, avg_fitness_per_gen)


"""
    (iv) Evolving to a target string with a larger alphabet (using a different fitness func and different mutation func)
"""
def part_iv():

    # setting the composition (what the string is made up of), target (e.g. target string or fitness score),
    # length of genomes, size of population
    composition = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = [0, 9, 8, 1, 5, 0, 0, 2, 1, 1, 2, 7, 6, 5, 5, 3, 0, 1, 1, 1, 9, 9, 9, 9, 8, 3, 2, 3, 0, 0]
    length = 30 # make sure length is the same size as target if target string is set as goal
    size = 200

    # completing evolution using functions from the gp_funcs class found in the other file
    gp = gp_funcs(composition, target, length, size)
    end_population, iterations, avg_fitness_per_gen = gp.evolution(
        gp.pop_generation, gp.part4_fitness, 
        gp.selection_function, gp.one_point_crossover, 
        gp.advanced_mutation, max_generations = 1000
    )

    # printing info to terminal and generating plots for this part
    print_statistics(end_population, target, iterations, "iv")
    plot_avgf_vs_gens("Part (iv)", iterations, avg_fitness_per_gen)


"""
    the function prints to terminal some information about each part,
    (could be commented out inside each part if not required, was helpful to check if everything works)
"""
def print_statistics(end_pop, target, iterations, part, extra = ""):

    print("%s\n" % n_spaces(120, "-", "\n\nThis is part ("+ part +"):"))
    print("\n The Target: '" + str(target) + "'" + extra)
    print("\n Number of Generations passed: " + str(iterations))
    print("\n Top 5 solutions for the last generation:\n ")

    for genome in end_pop[0:10]:
        print(genome)

 
"""
    the function will generate a plot with average fitness against generations
"""
def plot_avgf_vs_gens(name, iterations, avg_fitness_per_gen):

    plt.get_current_fig_manager().set_window_title(name)
    plt.plot(range(0,iterations+1), avg_fitness_per_gen)
    plt.xlabel("Generations")
    plt.ylabel("Average Fitness")
    plt.show()


"""
    function for for spacing things out in a cleaner manner
"""
def n_spaces(n, space = " ", extra = ""):
    spaces = "\n" + space*n + extra
    return spaces

"""
    main(), where the parts are run
"""
def assignment_part_1():

    print("\n---> Testing Environment <---")

    part_i()
    part_ii()
    part_iii()
    part_iv()

    print("%s" % n_spaces(120, "-"))

assignment_part_1()