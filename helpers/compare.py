from copy import deepcopy
from helpers.visualize import visualize

def compare(district):
    if len(district.disconnectedHouses) == 0 and \
            district.costs < district.compare.costs:
        district.compare = deepcopy(district)
        #visualize(district)
