# load classes and functions
from classes.classes import House, Battery, Cable
from functions.loadData import loadData
from functions.calculateCosts import calculateCosts
from functions.visualize import visualize
from functions.prompt import prompt

wijk, plot, sort = prompt()

# Specify paths for data to load
housePath = "data/wijk" + wijk + "_huizen.csv"
batteryPath = "data/wijk" + wijk + "_batterijen.txt"

# Load in data
houses, batteries = loadData(housePath, batteryPath)

# Sort houses by output
if sort == "y":
    houses.sort(key = lambda x: x.output)#, reverse = True)

# Connect all houses to nearest battery
for house in houses:
    house.connectNearestBattery(batteries)

# Calculate costs for this configuration
calculateCosts(houses, batteries)

if plot == "y":
    visualize(houses, batteries)
