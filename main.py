# load classes and functions
from classes.classes import *
from functions.loadData import loadData
from functions.calculateCosts import calculateCosts

# Specify paths for data to load
housePath = "data/wijk1_huizen.csv"
batteryPath = "data/wijk1_batterijen.txt"

# Load in data
houses, batteries = loadData(housePath, batteryPath)

# Connect all houses to nearest battery
for house in houses:
    house.connectNearestBattery(batteries)

# Show connection to batteries
for battery in batteries:
    battery.showConnections()

# Calculate costs for this configuration
calculateCosts(houses, batteries)
