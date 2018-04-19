# load classes and functions
from classes.classes import *
from functions.loadData import loadData
from functions.calculateCosts import calculateCosts
from functions.visualize import visualize


# Ask User which wijk to use, force 1,2 or 3 as input
wijk = input("Choose Wijk: ")
while wijk not in ["1","2","3"]:
    wijk = input("Choose Wijk(1, 2 or 3): ")

plot = input("Make plot?(y/n): " )
while plot not in ["y","n"]:
    plot = intput("Press y or n!")

# Specify paths for data to load
housePath = "data/wijk" + wijk + "_huizen.csv"
batteryPath = "data/wijk" + wijk + "_batterijen.txt"

# Load in data
houses, batteries = loadData(housePath, batteryPath)

# Connect all houses to nearest battery
for house in houses:
    house.connectNearestBattery(batteries)

# Calculate costs for this configuration
calculateCosts(houses, batteries)

if plot == "y":
    visualize(houses, batteries)
