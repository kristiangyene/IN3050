#!/usr/bin/env python3
from exhaustive_search import read_csv, get_distance

import sys
import csv
import random
import time
import statistics



def hill_climb(data, selected_cities):
    """Setting a random permutation as the current fastest route. Using the
    random.sample to get the same cities only with another order to see if its
    better than the current fastest. Doing this until there is no better solution 
    after 1000 evaluations. Method for finding a routes distance is taken from
    exhaustive_search.py.

    args:
        data (data (list): list containing a list of city names, and lists with city
        distances.)
        permutations (itertool object): object containing all possible 
        city combinations.

    return:
        shortest_tour (list): list containing the shortest tour found.
        shortest_distance (float): shortest distance found in float.

    """
    #Picking a random solution as the current best.
    shortest_tour = random.sample(selected_cities, len(selected_cities))
    shortest_distance = get_distance(data, shortest_tour)

    if(len(shortest_tour) > 1):

        fair_evaluations = 1000 #Number of evaluations
        worse_neighbors = 0

        #Compare to neighbor solution(s) and repeat until no better solution is found.
        while worse_neighbors <= fair_evaluations:
            copy = shortest_tour.copy()
            new_tour = swap_random_cities(copy) #Choose neighbor
            new_distance = get_distance(data, new_tour)

            if new_distance < shortest_distance:
                shortest_tour = new_tour
                shortest_distance = new_distance
                worse_neighbors = 0

            else: worse_neighbors += 1

    return shortest_tour, shortest_distance


def swap_random_cities(tour):
    """Gets the neighbor route by swapping two random cities in a route using 
    random.sample.

    args:
        tour (list): list containing a list of a tour(cities).

    return:
        tour (list): neighbor list with swapped cities. 

    """
    idx = range(len(tour))
    city1, city2 = random.sample(idx, 2)
    tour[city1], tour[city2] = tour[city2], tour[city1]
    return tour



def main():
    if(len(sys.argv) != 1):
        print("Wrong number of arguments..\nUsage: python3 hill_climbing.py")
        sys.exit(0)

    number_of_cities = int(input("How many cities?\n>"))

    if(number_of_cities <= 0 or number_of_cities > 24):
        print("Invalid number of cities.. Enter a number between 1 and 24")
        sys.exit(0)

    number_of_runs = int(input("How many algorithm running runs?\n>"))

    if(number_of_runs <= 0):
        print("Invalid number of runs.. Enter a number over 1")
        sys.exit(0)

    print("CALCULATING...")

    data, selected_cities = read_csv(number_of_cities)

    results = {}

    for i in range(number_of_runs):
        tour_result, distance_result = hill_climb(data, selected_cities)
        results[distance_result] = tour_result

    #Sorting the result-dict in a ascending order.
    sorted_results = dict(sorted(results.items()))

    #For easier print:
    sorted_cities = list(sorted_results.values())
    sorted_distances = list(sorted_results.keys())

    print("\n----------BEST RESULTS----------")
    print("Shortest tour:", sorted_cities[0], "\nTour distance: {0:.6f}km\n".format(sorted_distances[0]))

    print("\n----------WORST RESULTS----------")
    print("Longest tour:", sorted_cities[-1], "\nTour distance: {0:.6f}km\n".format(sorted_distances[-1]))


    print("Mean distance: {0:.6f}km".format(statistics.mean(sorted_distances)))
    if(len(sorted_distances) <= 1):
        print("standard deviation: {0:.6f}km". format(sorted_distances[0]))
    else: print("standard deviation: {0:.6f}km". format(statistics.stdev(sorted_distances)))



if __name__ == '__main__':
    start_time = time.time()
    main()
    result_time = time.time() - start_time
    print("Time result:   {0:.6f}s".format(result_time))


