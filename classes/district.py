import csv
from functions.hillclimber import hillclimber
from functions.visualize import visualize
from random import randint, shuffle


class District:

    def __init__(self, loadedData):
        self.houses = loadedData[0]
        self.batteries = loadedData[1]
        self.cables = set()
        self.costs = set()
        self.disconnectedHouses = []
        self.nthChoiceHouses = []

    def connectGreedy(self):
        for house in self.houses:
            house.connectNearestBattery(self.batteries, self)

    def connectRandom(self):
        for house in self.houses:
            house.connectRandomBattery(self.batteries, self)

    def saveVerbose(self,name):
        with open("configurations/" + name + ".txt", "w", newline="") as file:
            writer = csv.writer(file, dialect = "excel")
            writer.writerow(["configuration for " + name + " :"])
            writer.writerow([self.costs])
            writer.writerow(["\n"])
            writer.writerow(["---Battery-Stats---"])
            for battery in self.batteries:
                writer.writerow([str(battery)])
            writer.writerow(["\n"])
            writer.writerow(["---House-Stats---"])
            for house in self.houses:
                writer.writerow([str(house)])

    def save(self,name):
        with open("configurations/" + name + ".csv", "w", newline="") as file:
            writer = csv.writer(file, dialect = "excel")
            writer.writerow([self.costs])
            for battery in self.batteries:
                writer.writerow([battery.id,battery.capacity,battery.location[0],battery.location[1]])
            for house in self.houses:
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
        for house in self.houses:
            house.connection = set()
            house.distance = 1000
        for battery in self.batteries:
            battery.connectedHouses = []
            battery.capacity = battery.maxCapacity

    def calculateCosts(self):
        self.costs = 0
        for house in self.houses:
            if not house.distance == 1000:
                self.costs += house.distance * 9
        for battery in self.batteries:
            self.costs += battery.costs
        return self.costs


    def hillClimber(self):
        firstcosts = self.calculateCosts()

        for disconnectedHouse in self.disconnectedHouses:
            hillclimber(disconnectedHouse, self, 0, [])

        for nthChoiceHouse in self.nthChoiceHouses:
            if nthChoiceHouse.connection != "NOT CONNECTED!":
                hillclimber(nthChoiceHouse, self, 0, [])

        hillclimberHouses = self.houses
        shuffle(hillclimberHouses)

        for house in hillclimberHouses:
            if house.connection != "NOT CONNECTED!":
                hillclimber(house, self, 1, [])

        newcosts = self.costs
        print("This Configuration costs", newcosts, "€")

        if (newcosts < firstcosts or len(self.disconnectedHouses) != 0):
            # add simulated annealing?
            print("new hillclimber iteration")
            self.hillClimber()
        else:
            print("hillclimber finished")
            #self.save("hillclimberresults")
            return
