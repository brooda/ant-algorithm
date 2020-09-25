import re


# Parses the input
class InputParser:
    def __init__(self, config):
        self.numberOfTrucks = int(re.findall("Min no of trucks: \d+", config)[0].split("Min no of trucks: ")[1])
        self.optimalValue = int(re.findall("Optimal value: \d+", config)[0].split("Optimal value: ")[1])
        self.capacity = int(re.findall("CAPACITY : \d+", config)[0].split("CAPACITY : ")[1])

        self.cities = {}

        positions = re.findall("\d+ \d+ \d+", config)
        for pos in positions:
            pos = pos.split(" ")
            self.cities[int(pos[0]) - 1] = (int(pos[1]), int(pos[2]))

        self.demands = {}

        demandsRe = re.findall("\d+ \d+", config)
        for pos in demandsRe:
            pos = pos.split(" ")
            self.demands[int(pos[0]) - 1] = int(pos[1])