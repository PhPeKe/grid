# load classes and functions
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

    if args.method == "greedy":
        # Connect all houses to nearest battery
        district.connectGreedy()

    if args.method == "random":
        # Connect all houses to random battery
        district.connectRandom()
    print("Initial costs: ",district.calculateCosts())

    if args.part == "b":
        district.mode = "hillclimber-"
        district.hillClimber(False)
        district.mode = ""
        district = deepcopy(district.compare)
        district.calculateCosts()

    if args.part in ["b","c"]:
        district = kmeans(district, numIt = args.kmeansIt)

    if args.part in ["b","c","d"]:
        district = ultimate(district)

    print("Copy Costs: ",district.costs)
    if args.plot:
       visualize(district, True, "initial")

    kmeansIt = args.kmeansIt
    district = kmeans(district, numIt = kmeansIt)

    district = deepcopy(district.compare)

    district = ultimate(district)

    if args.save =="csv":
        district.save("District" + args.district)
    if args.save =="verbose":
        district.saveVerbose("District" + args.district)

    return district

if __name__ == "__main__":
    d = main()
