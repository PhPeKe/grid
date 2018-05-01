from calculateCosts import calculateCosts

def branchBound(district):
    """
    Takes a solution where all houses are connected and then tries to
    optimize with bounds
    """
    # Set initial upper bound (cost of the current configuration)
    upperBound = calculateCosts(district.houses, district.batteries)
    # Save initial configuration as best solution so far
    best = district
