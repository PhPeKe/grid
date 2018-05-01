# load classes and functions
from classes.classes import House, Battery, Cable, District
from functions.loadData import loadData
from functions.calculateCosts import calculateCosts
from functions.visualize import visualize
from functions.prompt import prompt
import sys

def main(argv):

    if not argv:
        districtNumber, plot, sort = prompt()

    elif not len(argv) == 3:
        sys.exit("You must enter none or 3 arguments")

    else:
        districtNumber, plot, sort = argv

    # Connection method executed by district, not implemented in prompt (yet)
    # --> Use random or greedy!
    method = "random"

    # Specify paths for data to load
    housePath = "data/wijk" + districtNumber + "_huizen.csv"
    batteryPath = "data/wijk" + districtNumber + "_batterijen.txt"

    # Load in data
    district = District(loadData(housePath, batteryPath))

    # Sort houses by output (ascending)
    if sort == "ya":
        district.houses.sort(key = lambda x: x.output)

    # Sort houses by output (descending)
    if sort == "yd":
        district.houses.sort(key = lambda x: x.output, reverse = True)

    if method == "greedy":
        # Connect all houses to nearest battery
        district.connectGreedy()
    elif method == "random":
        distric.connectRandom()

    # Calculate costs for this configuration
    district.calculateCosts()

    if plot == "y":
        visualize(district.houses, district.batteries)

    district.save("District" + districtNumber)

    return district

if __name__ == "__main__":
    district = main(sys.argv[1:])
