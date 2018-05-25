import csv
from algorithms.hillclimber import hillclimbSwitcher
from algorithms.ultimate import ultimate
from random import shuffle
from helpers.manhattan import manhattan
from copy import deepcopy
from helpers.acceptanceProbability import acceptanceprobability
from helpers.visualize import visualize
from random import random


class District:
    """District.py
        Class District
    """
    def __init__(self, loadedData):
        self.houses = loadedData[0]
        self.batteries = loadedData[1]
        self.cables = set()
        self.costs = set()
        self.disconnectedHouses = []
        self.nthChoiceHouses = []
        self.compare = set()
        self.allConnected = True
        self.mode = ""

    def connectGreedy(self, random = False):

        """Connect Greedy.

        Calls the method connectNearestBattery() in class Houses
        for all House-objectsin the House-list in District.

        When True is added the list of houses is sorted randomly
        before connections are made.
        """
        if random:
            shuffle(self.houses)
        for house in self.houses:
            house.connectNearestBattery(self.batteries, self)
        self.calculateCosts()

    def connectRandom(self):
        """Connect Random.

        Same Story as greedy but this time the connectRandomBattery()
        method in class Houses is called.
        """
        shuffle(self.houses)
        for house in self.houses:
            house.connectRandomBattery(self.batteries, self)
        self.calculateCosts()

    def save(self,name):
        with open("configurations/" + name + ".csv", "w", newline="") as file:
            writer = csv.writer(file, dialect = "excel")
            writer.writerow([self.costs])
            for battery in self.batteries:
                writer.writerow([battery.id,battery.capacity,battery.location[0],battery.location[1]])
            for house in self.houses:
                if house.connection != "NOT CONNECTED!":
                    if not house.connection == set():
                        writer.writerow([house.id,house.connection.id,house.output, house.location[0],house.location[1]])

    def load(self,name):
        infile = open("configurations/District1.csv")
        raw = infile.readlines()
        i = 0
        for objects in raw:
            self.houses = []
            self.batteries = []
            if i == 0:
                self.costs = objects
            if 0 < i < 5:
                temp = object.split(",")
                self.batteries.append(Battery())

    def disconnect(self):
        self.costs = set()
        self.disconnectedHouses = []
        self.nthChoiceHouses = []
        self.allConnected = True
        for house in self.houses:
            house.connection = set()
            house.distance = 1000
            house.possible_connections = []
        for battery in self.batteries:
            battery.connectedHouses = []
            battery.capacity = battery.maxCapacity
            battery.totalDistance = set()

    def calculateCosts(self):
        self.costs = 0
        for house in self.houses:
            if not house.distance == 1000:
                self.costs += house.distance * 9
        for battery in self.batteries:
            self.costs += battery.costs
        return self.costs

    def setClosestBattery(self):
        for b in self.batteries:
            b.closestBatteryDistance = 10000
            for b2 in self.batteries:
                distance = manhattan(b,b2)
                if b.maxCapacity == b2.maxCapacity and distance < b.closestBatteryDistance and not distance == 0:
                    b.closestBattery = b2
                    b.closestBatteryDistance = manhattan(b,b2)

    def hillClimber(self, sa):

        if self.compare == set():
            self.compare = deepcopy(self)

        unconnectCount = 0
        temperature = 500
        coolingRate = 0.9
        firstcosts = self.calculateCosts()
        iterationCount = 0

        while temperature > 1:
            iterationCount += 1
            visualize(self, True)
            for disconnectedHouse in self.disconnectedHouses:
                unconnectCount += 1
                hillclimbSwitcher(disconnectedHouse, self, True)

            for nthChoiceHouse in self.nthChoiceHouses:
                if nthChoiceHouse.connection != "NOT CONNECTED!":
                    hillclimbSwitcher(nthChoiceHouse, self)

            hillclimberHouses = self.houses
            shuffle(hillclimberHouses)

            for house in hillclimberHouses:
                if house.connection != "NOT CONNECTED!":
                    hillclimbSwitcher(house, self, 1)

            self.calculateCosts()

            print(self.costs, firstcosts, temperature)
            print(acceptanceprobability(self.costs - 1, firstcosts, temperature))
            if acceptanceprobability(self.costs - 1, firstcosts, temperature) <= random():
                break

            else:
                temperature *= coolingRate

            print("This Configuration's minimum costs:", self.compare.costs, "euro")
            firstcosts = self.costs


        print("hillclimber finished")
        self = deepcopy(self.compare)
        if len(self.disconnectedHouses) != 0:
            for house in self.disconnectedHouses:
                print("Could not connect house", house.id)
        return

    def ulti(self):
        ultimate(self)

    def compare(self):
        print(self.costs, self.compare.costs)
        if self.costs < self.compare.costs and len(self.disconnectedHouses) == 0:
            self.compare = deepcopy(self)
