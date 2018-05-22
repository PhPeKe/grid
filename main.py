# load classes and functions
from classes.house import House
from classes.battery import Battery
from classes.cable import Cable
from classes.district import District
from functions.helpers.loadData import loadData
from functions.visualize import visualize
from functions.switch import switch
from functions.algorithms.kmeans import kmeans
from functions.helpers.arguments import parseArgs
import sys
from random import shuffle
from copy import deepcopy

def main():

    # Get arguments
    args = parseArgs()

    # Specify paths for data to load
    housePath = "data/wijk" + args.district + "_huizen.csv"
    batteryPath = "data/wijk" + args.district + "_batterijen.txt"

    # Load in data
    district = District(loadData(housePath, batteryPath))

    # Sort houses by output (ascending)
    if args.sort == "ascending":
        district.houses.sort(key = lambda x: x.output)

    # Sort houses by output (descending)
    if args.sort == "descending":
        district.houses.sort(key = lambda x: x.output, reverse = True)


    # Sort houses random
    if args.sort == "random":
        shuffle(district.houses)

    if args.method == "greedy":
        # Connect all houses to nearest battery
        district.connectGreedy()

    if args.method == "random":
        # Connect all houses to random battery
        district.connectRandom()
    print("Initial costs: ",district.calculateCosts())
    visualize(district, False)
    district.hillClimber()
    district = deepcopy(district.compare)
    # Calculate costs for this configuration
    district.calculateCosts()

    print("Costs: ",district.costs)
    if args.plot:
        visualize(district, True, 1)

    i = 0
    while (i < 10):
        kmeans(district)
        district.disconnect()
        district.connectGreedy()
        district.hillClimber()
        kmeans(district)
        visualize(district, True, numIt = str(i))
        i += 1

    if args.save =="csv":
        district.save("District" + args.district)
    if args.save =="verbose":
        district.saveVerbose("District" + args.district)

    return district, args

if __name__ == "__main__":
    district, args = main()
