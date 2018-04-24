# load classes and functions
from classes.classes import House, Battery, Cable
from functions.loadData import loadData
from functions.calculateCosts import calculateCosts
from functions.visualize import visualize
from functions.prompt import prompt
import sys

def main(argv):

    if not argv:
        district, plot, sort = prompt()
    elif not len(argv) == 3:
        sys.exit("You must enter none or 3 arguments")
    else:
        district, plot, sort = argv
        
    # Specify paths for data to load
    housePath = "data/wijk" + district + "_huizen.csv"
    batteryPath = "data/wijk" + district + "_batterijen.txt"

    # Load in data
    houses, batteries = loadData(housePath, batteryPath)

    # Sort houses by output (ascending)
    if sort == "ya":
        houses.sort(key = lambda x: x.output)

    # Sort houses by output (descending)
    if sort == "yd":
        houses.sort(key = lambda x: x.output, reverse = True)

    # Connect all houses to nearest battery
    for house in houses:
        house.connectNearestBattery(batteries)

    # Calculate costs for this configuration
    calculateCosts(houses, batteries)

    if plot == "y":
        visualize(houses, batteries)

if __name__ == "__main__":
    main(sys.argv[1:])
