from random import choices, randint, randrange, random

class gp_funcs:

    """
        Class constructor:

        parameters:
        --> composition, defines if only 1's & 0's are used or if extra digits are used (0 - 9)
        --> target, our target fitness or target string
        --> length, length of generated genome string
        --> size, size of population
    """
    def __init__(self, composition, target, length, size):
        self.composition = composition
        self.target = target
        self.length = length
        self.size = size
        self.easter_egg = 0


    """
        function in charge of generating a genome from 1's and 0's or other digits of length k.
    """
    def genome_generation(self):
        return choices(self.composition, k=self.length)
    

    """
        function in charge of creating a population, using the genome_generation function,
        multiple times to create a population of size n.
    """
    def pop_generation(self):
        return [self.genome_generation() for n in range(self.size)]


    """
        simple fitness function for 'part-one' or '(i)', that does not take into account
        a target string. ("simple fitness function" or "part1_fitness")

        parameters:
        --> genome, is the array of 0's, 1's.
    """
    def simple_fitness(self, genome):

        num_of_ones = 0
        genome_length = len(genome)

        for gene in genome:
            if gene > 0:
                num_of_ones += 1
       
        fitness = (num_of_ones / genome_length)
        if fitness == self.target:
            return 1.0

        return fitness


    """
        fitness function for 'part-two' or '(ii)', that does take into account
        a target string of 0's and 1's.

        parameters:
        --> genome, is the array of 0's, 1's.
    """
    def part2_fitness(self, genome):

        num_matches = 0
        genome_length = len(genome)

        for i, gene in enumerate(genome):
            if gene == self.target[i]:
                num_matches += 1

        return (num_matches / genome_length)


    """
        fitness function for 'part-three' or '(iii)', that does not take into account
        a target string of 0's and 1's. Instead it is similar to simple_fitness, and
        it also returns '2*(length of the solutions) / genome_length' if all genes in genome are 0's

        parameters:
        --> genome, is the array of 0's, 1's.
    """
    def part3_fitness(self, genome):

        num_of_ones = 0
        genome_length = len(genome)

        for gene in genome:
            if gene > 0:
                num_of_ones += 1

        # In this case, the fitness should be '2*(length of the solutions)',
        # hence '2*(length of the solutions) / genome_length', to keep the
        # returned fitness percentages in similar units that don't deviate too much
        # since when all are 1's, (length of the solutions) / genome_length = 1.0.
        # therefore, 2*(length of the solutions) / genome_length = 2.0
        if num_of_ones == 0:
            return 2.0 
       
        fitness = (num_of_ones / genome_length)
        if fitness == self.target:
            return 1.0 

        return fitness


    """
        fitness function for 'part-four' or '(iv)', that does take into account
        a target string of all digits. Basically identical to the part2 fitness function
        just this one will be used for digits, however the other can also be used this way

        parameters:
        --> genome, is the array of 0's, 1's, 2's, 3's, 4's and so on.
    """
    def part4_fitness(self, genome):

        num_matches = 0
        genome_length = len(genome)

        for i, gene in enumerate(genome):
            if gene == self.target[i]:
                num_matches += 1
            # elif 

        # least distance 

        return (num_matches / genome_length)


    """
        selection function - select pair of solutions which will be
        the parents of the two new solutions for the next generation

        parameters:
        --> population, an array of genomes
        --> fitness_func, is any of the available fitness functions
    """
    def selection_function(self, population, fitness_func):
        
        # solutions with a higher fitness should be more likely to be chosen, 
        # hence the use of weights
        return choices(
            population,
            weights=[fitness_func(genome) for genome in population],
            k=2 # simply means that we draw twice to get a pair from the population
        )


    """
        one point crossofver function - takes two genomes and slices
        each of them at a random index and then swaps a part of each
        genome with the other.
    """
    def one_point_crossover(self, genome_a, genome_b):

        # return if the Genomes are not atleast 2 in length, 
        # or if one of the genomes is less than 2 in length
        length = 2
        length_a, length_b = len(genome_a), len(genome_b)
        if (length_a < length > length_b) or (length_a != length_b):
            return genome_a, genome_b
        else:
            length = length_a

        cut_index = randint(1, length - 1)
        return genome_a[0:cut_index] + genome_b[cut_index:], genome_b[0:cut_index] + genome_a[cut_index:]

    """
        standard mutation function, not as efficient if more than just
        binary digits are used, however it can still be used for them

        parameters:
        --> num_rounds - extra rounds increase the probability of mutation
        --> probability - just the chance of a succesfull mutation
    """
    def standard_mutation(self, genome, num_rounds = 1, probability = 0.2):

        for _ in range(num_rounds):

            index = randrange(len(genome))
            if random() < probability:
                genome[index] = abs(genome[index] - 1)

        return genome

    """
        advanced mutation function for 'part-four' or '(iv)' - can be used both for 
        only binary 0's and 1's and also for other digits, just like the standard one,
        however, this advanced mutation function will give the mutations more influence if digits
        other than 0's and 1's are used. 

        parameters:
        --> num_rounds - extra rounds increase the probability of mutation
        --> probability - just the chance of a succesfull mutation
    """
    def advanced_mutation(self, genome, num_rounds = 1, probability = 0.2):

        for _ in range(num_rounds):

            index = randrange(len(genome))
            if random() < probability:
                genome[index] = abs(genome[index] - choices(self.composition, k=1)[0])

        return genome

    """
        evolution function - simply uses all the above functions and follows the genetic programming process
    """
    def evolution(
        self, pop_gen_func,
        fitness_func, selection_func,
        crossover_func, mutation_func,
        max_generations = 100, test_part3 = False
    ):
        
        # generate population, and reset it to below if testing part3 of assignment 1 part 1
        population = pop_gen_func()
        if test_part3 is True:
            population = [
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 1]
            ]

        avg_fitness_per_generation = []
        for i in range(max_generations):

            population = sorted(
                population,
                key=lambda genome: fitness_func(genome),
                reverse=True
            )

            # get fitness for each genome in generation and then just get avg fitness using this
            total_fitness = 0
            for genome in population:
                total_fitness += fitness_func(genome)
            avg_fitness_per_generation += [(total_fitness / len(population))]

            # reached our fitness limit/goal
            if fitness_func(population[0]) == 1.0 or fitness_func(population[0]) == 2.0:
                break

            next_gen = population[0:2] # just keep the top two genomes for the next generation

            # now it is time to generate all other genomes for the next generation
            for _ in range(int(len(population) / 2) - 1):
                parents = selection_func(population, fitness_func) # get parents (length is halved so only looping for half the length)
                child_a, child_b = crossover_func(parents[0], parents[1])
                child_a = mutation_func(child_a) # child a undergoes mutation with % chance of success
                child_b = mutation_func(child_b) # child b undergoes mutation with % chance of success
                next_gen += [child_a, child_b] # new genomes are added to the next_gen of genomes

            population = next_gen # the next generation is now the population

        # sort the population again in the case that this is the last iteration
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        # return the population and the number of iterations it took to reach the fitness limit
        return population, i, avg_fitness_per_generation
