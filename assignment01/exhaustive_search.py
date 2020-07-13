import sys
import csv
import itertools
import time


"""A program that selects the shortest possible tour among a subset of cities.
The problem is solved by using exhaustive search that is guaranteed to find the 
best suited(shortest) tour for the TSP problem."""


def get_distance(data, combination):
    """Iterates through a tour and sums up all the distances between every city.

    args:
        data (list): list containing a list of city names, and lists with city
        distances.
        combination (list): list containing one permutation of citites.

    return:
        final_distance (float): the distance in one particular tour.
    """
    final_distance = 0
    for i in range(len(combination) - 1):
        from_city = data[0].index(combination[i])
        to_city = data[0].index(combination[i + 1])
        distances = data[1:]
        distance = float(distances[from_city][to_city])
        final_distance += distance
    
    last_city = data[0].index(combination[-1])
    first_city = data[0].index(combination[0])
    last_distance = float(data[1:][last_city][first_city])
    final_distance += last_distance
    return final_distance


def find_shortest(data, permutations):
    """Iterates through all possible tours between all cities and finds the 
    shortest one.

    args:
        data (list): list containing a list of city names, and lists with city
        distances.
        permutations (itertool object): object containing all possible 
        city combinations.
    
    return:
        shortest_tour (list): list containing the shortest possible tour.
        shortest_distance (float): shortest possible distance in float.

    """
    shortest_tour = []
    shortest_distance = 0
    #Iterate through all possible tours between a set of cities.
    for tour in permutations:
        combination = list(tour)
        distance = get_distance(data, combination)
        #Check if the path is currently the shortest.
        if(shortest_distance == 0 or distance < shortest_distance):
            shortest_tour = combination
            shortest_distance = distance
    return shortest_tour, shortest_distance


def read_csv(number_of_cities):
    """Reads and gather information from the csv-file with information about the 
    city and the distances between them.

    args:
        number_of_cities (String): name of the csv-file containing city 
        information.

    return:
        data (list): list containing a list of city names, and lists with city
        distances.
        selectes_cities (list): list with the chosen cities.

    """

    file = open("european_cities.csv", "r")
    data = list(csv.reader(file, delimiter=";"))
    selected_cities = data[0][0:number_of_cities]

    return data, selected_cities


def main():
    if(len(sys.argv) != 1):
        print("Wrong number of arguments..\nUsage: python3 exhaustive_search.py")
        sys.exit(0)

    number_of_cities = int(input("How many cities do you want?\n>"))

    if(number_of_cities <= 0 or number_of_cities > 24):
        print("Invalid number of cities.. Enter a number between 1 and 24")
        sys.exit(0)

    print("CALCULATING...")
    data, selected_cities = read_csv(number_of_cities)
    permutations = itertools.permutations(selected_cities)
    shortest_tour, shortest_distance = find_shortest(data, permutations)
    shortest_tour.append(shortest_tour[0])
    print("\nShortest tour:", shortest_tour, "\nTour distance: {0:.6f}".format(shortest_distance))


if __name__ == '__main__':
    start_time = time.time()
    main()
    result_time = time.time() - start_time
    print("Time result:   {0:.6f}s".format(result_time))


