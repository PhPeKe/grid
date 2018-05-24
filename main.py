# load classes and functions
from classes.house import House
from classes.battery import Battery
from classes.cable import Cable
from classes.district import District
from functions.helpers.loadData import loadData
from functions.visualize import visualize
from functions.switch import switch
from functions.algorithms.kmeans import kmeans
from functions.ultimate import ultimate
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
    district.hillClimber()
    ultimate(district)
    district = deepcopy(district.compare)

    # Calculate costs for this configuration
    district.calculateCosts()

    print("Costs: ",district.costs)
    if args.plot:
        visualize(district, True, "initial")

    plotIndex = 0

    district, plotIndex = kmeans(district, numIt = 50, plotIndex = plotIndex)
    district, plotIndex = kmeans(district, numIt = 50, plotIndex = plotIndex)

    if args.save =="csv":
        district.save("District" + args.district)
    if args.save =="verbose":
        district.saveVerbose("District" + args.district)

    return district

if __name__ == "__main__":
    d = main()
