from copy import deepcopy
from helpers import visualize

def compare(district):
    if district.costs < district.compare.costs and len(district.disconnectedHouses) == 0:
        district.compare = deepcopy(district)
        #visualize(district)