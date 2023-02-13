import random
import pandas as pd
import matplotlib.pyplot as plt

def unpack_data(student_file, supervisor_file):

        # Load in the data for the two files
        students = pd.read_excel(student_file, header=None)
        supervisors = pd.read_excel(supervisor_file, header=None)

        # remove unnecessary items
        students = students.iloc[: , 1:]
        supervisors = supervisors.iloc[: , 1:]

        # format as dictionary
        students_dict = students.transpose().to_dict()
        supervisors_dict = supervisors.to_dict()       

        # format as arrays
        students_array = students.to_numpy()
        supervisors_array = supervisors.to_numpy().flatten()

        # # Convert each row of the numpy array into a list of student preferences
        students_array = [list(students_array[i]) for i in range(students_array.shape[0])]

        return [students_dict, supervisors_dict, students_array, supervisors_array]


"""
    the function prints to terminal some information about each part,
    (could be commented out inside each part if not required, was helpful to check if everything works)
"""
def print_statistics(king, worst, best, target, iterations, part, extra = ""):

    print("%s\n" % n_spaces(120, "-", "\n\nThis is part ("+ part +"):"))
    print("\n The Target: '" + str(target) + "'" + extra)
    print("\n Number of Generations passed: " + str(iterations))
    print("\n The best fitness: " + str(best))
    print("\n The worst fitness: " + str(worst))
    print("\n Top 1 solution:\n\n " + str(king))


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


class gp_funcs:

    def __init__(self, student_file, supervisor_file, population_size):
        data = unpack_data(student_file, supervisor_file)
        self.student_choices = data[0]
        self.supervisor_capacities = data[1]
        self.student_array = data[2]
        self.supervisor_array = data[3]
        self.population_size = population_size


    def generate_initial_population(self):
        population = []
        for i in range(self.population_size):
            mapping = {}
            supervisors_capacity = self.supervisor_array.copy()
            # print("soup capacity: %s" % str(supervisors_capacity))
            # print("the students: %s" % str(self.student_array))
            # print("length of students: %d" % len(self.student_array))
            for student in range(len(self.student_array)):
                available_lecturers = [index for index, capacity in enumerate(supervisors_capacity) if capacity > 0]
                # print(available_lecturers)
                lecturer = random.choice(available_lecturers)
                mapping[student] = lecturer + 1
                supervisors_capacity[lecturer] -= 1
            population.append(mapping)
        return population


    def fitness_function(self, genome):

        # the lower the fitness the better so this should increment by 1 each time it is worse
        fitness = 0

        choices = self.student_choices # this is students_dict
        lecturer_capacity = self.supervisor_capacities.copy() # this is the array of lecturer capacities
        lecturer_counts = [0] * len(lecturer_capacity[1])# to keep track of how many students are assigned to each lecturer

        for student, lecturer in genome.items():

            current_std = choices[student]
            # print("\nWanted: '%d', Got: '%d'\n" % (current_std[1], lecturer))

            for index, ranking in enumerate(current_std.values()):

                current = index + 1

                if current == lecturer:
                    fitness += (ranking - 1)
                    break
            
            lecturer_counts[lecturer-1] += 1
            
        # checking if the capacity has been exceeded for any of the lecturers
        for i, count in enumerate(lecturer_counts):

            if count > lecturer_capacity[1][i]:
                fitness += 100

        return (fitness / len(genome))
    

    def tournament_selection(self, population, fitness_array):
        tournament_participants = random.sample(population, 4)
        tournament_fitness = [fitness_array[population.index(pos)] for pos in tournament_participants]
        # Select the best individual from the tournament
        return tournament_participants[tournament_fitness.index(min(tournament_fitness))]


    def crossover(self, parent1, parent2):
        
        # Choose a random crossover point
        split_point = random.randint(1, len(parent1) - 1)
        # Get list of keys for both parents
        keys1 = list(parent1.keys())
        keys2 = list(parent2.keys())
        # Split first parent into two lists of keys
        first_keys1 = keys1[:split_point]
        second_keys1 = keys1[split_point:]
        # Split second parent into two lists of keys
        first_keys2 = keys2[:split_point]
        second_keys2 = keys2[split_point:]
        # Create smaller dictionaries out of key lists for parent 1
        parent1_dict1 = {key: parent1[key] for key in first_keys1}
        parent1_dict2 = {key: parent1[key] for key in second_keys1}
        # Create smaller dictionaries out of key lists for parent 2
        parent2_dict1 = {key: parent2[key] for key in first_keys2}
        parent2_dict2 = {key: parent2[key] for key in second_keys2}
        # Create offspring from split dictionaries
        parent1_dict1.update(parent2_dict2)
        parent2_dict1.update(parent1_dict2)
        # Return offpsring
        return parent1_dict1, parent2_dict1


    def swapper_mutation(self, genome, num_rounds = 1, probability = 0.4):

        for _ in range(num_rounds):

            # based on probability do the following
            if random.random() < probability:

                # get to random positions
                pos1 = random.randrange(len(genome))
                pos2 = random.randrange(len(genome))

                # make sure positions are not equal
                if (pos1 != pos2):

                    # print("\nmutation on '%s' in progress: \n" % str(genome))
                    # print("positions to be swapped: '%d' & '%d'" % (pos1, pos2))

                    # get the values from the target positions
                    pos1_val = genome[pos1]
                    pos2_val = genome[pos2]

                    # carry out the swap
                    genome[pos1] = pos2_val # value at pos2 submitted into pos1
                    genome[pos2] = pos1_val # value at pos1 submitted into pos2

                    # print("\nmutated genome: '%s'\n" % str(genome))

        return genome


    def evolution(
        self, gen_init_pop_func, fitness_func,
        tournament_func, crossover_func,
        mutation_func, GENERATIONS = 100,
    ):
        # generate init pop & initialise fitness array
        population = gen_init_pop_func()
        fitness_array = []
        best_fitness = 100
        worst_fitness = 0
        king = {}

        # run evolution and initialise the avg fitness array
        avg_fitness_per_generation = []
        for i in range(GENERATIONS):

            population = sorted(
                population,
                key=lambda genome: fitness_func(genome),
                reverse=False
            )

            # get fitness for each genome in generation and then just get avg fitness using this
            total_fitness = 0
            for genome in population:
                fitness = fitness_func(genome)
                fitness_array.append(fitness)

                # statement that will save this
                if best_fitness > fitness:
                    king = genome

                best_fitness = min(best_fitness, fitness)
                worst_fitness = max(worst_fitness, fitness)
                total_fitness += fitness
            avg_fitness_per_generation += [(total_fitness / len(population))]

            # reached our fitness limit/goal
            if fitness_func(population[0]) == 0.00:
                break

            # keep top two genomes for the next generation, a test populations fitness
            new_population = []
            for _ in range(int(len(population) / 2)):

                # pick parents and perform crossover
                parent1 = tournament_func(population, fitness_array)
                parent2 = tournament_func(population, fitness_array)
                child1, child2 = crossover_func(parent1,parent2)

                # expose to mutations
                child1 = mutation_func(child1)
                child2 = mutation_func(child2)

                # append the children to the new population
                new_population.append(child1)
                new_population.append(child2)

            population = new_population

        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=False
        )
        
        return king, i, avg_fitness_per_generation, best_fitness, worst_fitness


def main():

    student_file, supervisor_file = "Student-choices.xlsx", "Supervisors.xlsx"
    population_size = 12
    target = 0.0

    # to use functions
    gp = gp_funcs(student_file, supervisor_file, population_size)

    # run evolution
    king, iterations, avg_fitness_per_gen, best_fitness, worst_fitness = gp.evolution(
        gp.generate_initial_population, 
        gp.fitness_function, gp.tournament_selection, 
        gp.crossover, gp.swapper_mutation, 20000
    )

    # printing info to terminal and generating plots for this part
    print_statistics(king, worst_fitness, best_fitness, round(target, 1), iterations, "Statistics Info")
    plot_avgf_vs_gens("Part two of Assignment 1", iterations, avg_fitness_per_gen)


main()
