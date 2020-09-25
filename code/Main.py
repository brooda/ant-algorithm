from InputParser import *
from Helpers import *
import numpy as np
import coefficients
import  matplotlib.pyplot as plt
from itertools import chain

np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

class AntAlgorithm:
    def __init__(self, input_file, iterations):
        with open(input_file, "r") as file:
            config = file.read()

        input_parsed = InputParser(config)
        self.number_of_cities = len(input_parsed.cities)
        self.cities = input_parsed.cities

        # Create distance matrix
        self.dists = np.zeros((self.number_of_cities, self.number_of_cities))
        for i in range(self.number_of_cities):
            for j in range(i, self.number_of_cities):
                posI = input_parsed.cities[i]
                posJ = input_parsed.cities[j]

                self.dists[i, j] = np.sqrt(np.power(posI[0] - posJ[0], 2) + np.power(posI[1] - posJ[1], 2))
                self.dists[j, i] = self.dists[i, j]

                # To avoid dividing per 0
                if i == j:
                    self.dists[i, j] = 0.001

        # Create proximity matrix
        self.ni = 1 / self.dists

        # Init pheromone trail
        self.pheromone_trail = np.zeros((self.number_of_cities, self.number_of_cities))
        for i in range(self.number_of_cities):
            for j in range(i + 1, self.number_of_cities):
                self.pheromone_trail[i, j] = np.random.rand() / 100
                self.pheromone_trail[j, i] = self.pheromone_trail[i, j]

        # Init capacity and demands
        self.capacity = input_parsed.capacity
        self.demands = input_parsed.demands

        # Optimal value
        self.optimal_value = input_parsed.optimalValue
        
        # Set the number of iterations to run
        self.iterations = iterations

    # Returns index of a city where ant should go based on probability distribution
    def choose_next_city(self, current_city, available_cities):
        row_ni = np.take(self.ni[current_city], available_cities)
        row_ni = np.power(row_ni, coefficients.Beta)

        row_pheromone_trail = np.take(self.pheromone_trail[current_city], available_cities)
        row_pheromone_trail = np.power(row_pheromone_trail, coefficients.Alfa)

        product = np.dot(row_ni, row_pheromone_trail)

        probabilities = np.multiply(row_ni, row_pheromone_trail) / product
        cumulative_sum = np.cumsum(probabilities)

        rand = np.random.rand()
        for counter, val in enumerate(cumulative_sum):
            if val >= rand:
                return available_cities[counter]

        return 0

    def filter_cities_that_cant_be_served(self, available_cities, stock):
        return list(filter(lambda x: self.demands[x] <= stock, available_cities))

    def cost_of_path(self, path):
        cost = 0
        for i in range(len(path)-1):
            cost += self.dists[path[i], path[i+1]]
        return cost

    def deposit_pheromones(self, path):
        len_of_path = self.cost_of_path(path)
        add = coefficients.Q / len_of_path

        for i in range(len(path)-1):
            self.pheromone_trail[path[i], path[i+1]] += add
            self.pheromone_trail[path[i + 1], path[i]] += add

    def get_path_for_ant(self):
        path = []
        current_city = 0
        path.append(current_city)
        stock = self.capacity
        not_visited_cities = [j for j in range(1, self.number_of_cities)]

        # We start from the depot until we will visit all the cities
        while len(not_visited_cities) > 0:
            available_cities = self.filter_cities_that_cant_be_served(not_visited_cities, stock)

            if len(available_cities) == 0:
                stock = self.capacity
                path.append(0)
                current_city = 0
                continue

            # We are choosing next city based on probability distribution
            city_to_go_next = self.choose_next_city(current_city, available_cities)
            path.append(city_to_go_next)
            not_visited_cities.remove(city_to_go_next)
            stock -= self.demands[city_to_go_next]
            current_city = city_to_go_next

        return path

    def evaporate(self):
        self.pheromone_trail *= coefficients.EvaporationRate
        self.pheromone_trail[self.pheromone_trail < 0.00000001] = 0.00000001

    def solve(self):
        shortest_path_cost = 10 ** 8

        # More iterations == more learning
        for iter in range(self.iterations):
            paths = []

            # In each iteration we rum more than one ant.
            # It is shown, that it is good, when number of ants is the same like number of cities.
            for ant in range(self.number_of_cities):
                paths.append(self.get_path_for_ant())

            # Evaporate
            self.evaporate()

            for path in paths:
                self.deposit_pheromones(path)

            for path in paths:
                if self.cost_of_path(path) < shortest_path_cost:
                    shortest_path_cost = self.cost_of_path(path)
                    best_path = path

        return shortest_path_cost, best_path

for path in input_paths():
    filename = (path[path.index('\\') + 1: path.rfind('.')])
    print(filename)
    alg = AntAlgorithm(path, 500)

    shortest_path_cost, best_path = alg.solve()
    print("Optimal: ", alg.optimal_value, "my: ", shortest_path_cost, "ratio: ", shortest_path_cost/alg.optimal_value)


# Test dependance on iterations
'''
for path in input_paths():
    ratios = []
    iterations = []
    for number_of_iterations in chain(range(5, 45, 5), range(50, 2000, 50)):
        print(number_of_iterations)
        alg = AntAlgorithm(path, number_of_iterations)
        shortest_path_cost, best_path = alg.solve()
        ratio = shortest_path_cost/alg.optimal_value

        iterations.append(number_of_iterations)
        ratios.append(ratio)
    plt.plot(iterations, ratios)
    plt.show()
    break
'''