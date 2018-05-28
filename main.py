# load classes and functions
from classes.house import House
from classes.battery import Battery
from classes.district import District
from helpers.loadData import loadData
from helpers.visualize import visualize
from algorithms.kmeans import kmeans
from algorithms.ultimate import ultimate
from helpers.arguments import parseArgs
from random import shuffle
from copy import deepcopy

def main():
    """ Smart Grid by Groep 1

        Please refer to the README for more information.

    """

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


    if args.part == "a":
        if args.method == "greedy":
            # Connect all houses to nearest battery
            district.connectGreedy()
            print("Initial costs: ",district.calculateCosts())

        if args.method == "random":
            # Connect all houses to random battery
            district.connectRandom()

        if args.plot:
           visualize(district, True, "Initial")

    if args.part == "b":
        if args.method == "greedy":
            # Connect all houses to nearest battery
            district.connectGreedy()
            print("Initial costs: ",district.calculateCosts())

        if args.method == "random":
            # Connect all houses to random battery
            district.connectRandom()

        if args.plot:
           visualize(district, True, "Initial")
        district.hillClimber()
        if args.plot:
           visualize(district, True, "After hillclimber")

    if args.part == "c":
        if args.method == "greedy":
            # Connect all houses to nearest battery
            district.connectGreedy()
            print("Initial costs: ",district.calculateCosts())

        if args.method == "random":
            # Connect all houses to random battery
            district.connectRandom()

        if args.plot:
           visualize(district, True, "Initial")
        district.hillClimber()
        if args.plot:
           visualize(district, True, "After hillclimber")

        kmeansIt = args.kmeansIt
        district = kmeans(district, numIt = args.kmeansIt)

        if args.plot:
           visualize(district, True, "After kmeans")

    if args.part == "d":
        if args.method == "greedy":
            # Connect all houses to nearest battery
            district.connectGreedy()
            print("Initial costs: ",district.calculateCosts())

        if args.method == "random":
            # Connect all houses to random battery
            district.connectRandom()

        if args.plot:
           visualize(district, True, "Initial")

        district.hillClimber()

        if args.plot:
           visualize(district, True, "After hillclimber")

        kmeansIt = args.kmeansIt
        district = kmeans(district, numIt = args.kmeansIt)
        if args.plot:
           visualize(district, True, "After kmeans")

        district = ultimate(district)

    print("Costs: ",district.costs)

    if args.plot:
       visualize(district, True, "Final")

    if args.save =="csv":
        district.save("District" + args.district)

    return district

if __name__ == "__main__":
    d = main()
