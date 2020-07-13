#!/usr/bin/env python3
from exhaustive_search import read_csv, get_distance

import sys
import csv
import random
import time
import statistics
import numpy as np
import pandas as pd


#Help functions
#-----------------------------------------------------

def calculate_fitness(individual, population):
    total_distance = total_distance(population)
    return total_distance / individual[1]


def total_distance(population):
    total_distance = 0
    for i in range(len(population)):
        total_distance += population[i][1]
    return total_distance


def total_fitness(population):
    total_fitness = 0
    for i in range(len(population)):
        total_fitness += population[i][2]
    return total_fitness

#-----------------------------------------------------


#Selection functions
#-----------------------------------------------------

def survivor_selection(population, population_size):
    population.sort(key=lambda x: x[2], reverse=True)
    while len(population) > population_size:
        population.pop()


def parent_selection(population):
    selected = None
    i = random.randint(0, len(population) - 1)
    while selected == None:
        if i == len(population):
            i = 0

        #Selecting parents based on fitness
        rand = random.uniform(0, 1)
        chance = population[i][2] / total_fitness(population)
        if(rand < chance):
            selected = population[i]
        i += 1

    return selected

#-----------------------------------------------------


#Recombination and mutation functions
#-----------------------------------------------------

def pmx(parent1, parent2, start, stop, data):
    child = [None] * len(parent1)
    child[start:stop] = parent1[start:stop]
    
    for ind, x in enumerate(parent2[start:stop]):
        ind += start
        if x not in child:
            while child[ind] != None:
                ind = parent2.index(parent1[ind])
            child[ind] = x

    for ind, x in enumerate(child):
        if x == None:
            child[ind] = parent2[ind]

    return [child, get_distance(data, child), 0]


def pmx_pair(parent1, parent2, data):
    parent1 = parent1[0]
    parent2 = parent2[0]
    
    half = len(parent1) // 2
    start = np.random.randint(0, len(parent1) - half)
    stop = start + half

    return pmx(parent1, parent2, start, stop, data), pmx(parent2, parent1, start, stop, data)


def swap_mutate(child, data):
    route = child[0]

    cities = np.random.choice(len(route), 2, replace=False)
    route[cities[0]], route[cities[1]] = route[cities[1]], route[cities[0]]

    return [route, get_distance(data, route), 0]

#-----------------------------------------------------


#Generation functions
#-----------------------------------------------------

def next_generation(population, data):
    population_size = len(population)

    offspring = []
    for i in range(len(population) // 2):

        #Setting parents
        p1 = parent_selection(population)
        p2 = parent_selection(population)
        
        #Do crossovers
        c1, c2 = pmx_pair(p1, p2, data)

        #Do mutating 
        c1 = swap_mutate(c1, data)
        c2 = swap_mutate (c2, data)

        offspring.append(c1)
        offspring.append(c2)

    for route in offspring:
        route[2] = total_distance(offspring) / route[1]
    
    population += offspring
    
    survivor_selection(population, population_size)


def generation_generator(population, data):
    number_of_generations = 0
    current_best = population[0]
    no_improvements = 0
    #fitness_gen = []

    while(no_improvements < 100):
        #fitness_gen.append(population[0][2])
        next_generation(population, data)
        number_of_generations += 1

        if(population[0][1] < current_best[1]):
            current_best = population[0]
            no_improvements = 0
        else: no_improvements += 1

    #df = pd.DataFrame(fitness_gen)
    #df.to_excel('output.xlsx', header=False, index=False) 

    return number_of_generations, no_improvements

#-----------------------------------------------------



def create_population(size, selected_cities, data):
    population = []
    for i in range(size):
        copy = selected_cities.copy()
        random.shuffle(copy)
        #Individual: ([route], distance, fitness)
        population.append([copy, get_distance(data, copy), 0])

    for i in range(len(population)):
        population[i][2] = total_distance(population) / population[i][1]


    return population


def main():
    if(len(sys.argv) != 1):
        print("Wrong number of arguments..\nUsage: python3 genetic_algorithm.py")
        sys.exit(0)

    number_of_cities = int(input("How many cities?\n>"))

    if(number_of_cities <= 1 or number_of_cities > 24):
        print("Invalid number of cities.. Enter a number between 2 and 24")
        sys.exit(0)

    print("CALCULATING...")

    data, selected_cities = read_csv(number_of_cities)

    population_sizes = [30, 60, 90] #Selected population sizes

    best_candidates = []

    for i in range(len(population_sizes)):
        population = create_population(population_sizes[i], selected_cities, data)
        number_of_generations, no_improvements = generation_generator(population, data)
        best_candidates.append(population[0])

        results = {}
        fitness = []
        for j in population:
            results[j[1]] = j[0]
            fitness.append(j[2])
        
        #Sorting the result-dict in a ascending order.
        sorted_results = dict(sorted(results.items()))

         #For easier print:
        sorted_cities = list(sorted_results.values())
        sorted_distances = list(sorted_results.keys())

        
        sorted_fitness = sorted(fitness, reverse=True)

        print("\n------ POPULATION SIZE:", population_sizes[i], "------")
        print("Number_of_generations:", number_of_generations - no_improvements)
        print("Best individual stats:\n\troute:", sorted_cities[0], 
        "\n\tDistance:", sorted_distances[0], "\n\tFitness: {0:.3f}".format(sorted_fitness[0]))
        print("Worst distance:", sorted_distances[-1])
        print("Mean distance: {0:.6f}km".format(statistics.mean(sorted_distances)))
        if(len(sorted_distances) <= 1):
            print("standard deviation: {0:.6f}km". format(sorted_distances[0]))
        else: print("standard deviation: {0:.6f}km". format(statistics.stdev(sorted_distances)))


if __name__ == '__main__':
    start_time = time.time()
    main()
    result_time = time.time() - start_time
    print("Time result:   {0:.6f}s".format(result_time))


