from functions.calculateCosts import calculateCosts
from functions.switch import switch
from random import randint, shuffle


def branchBound(district):
    """
    Takes a solution where all houses are connected and then tries to
    optimize with bounds
    """
    # Set initial upper bound (cost of the current configuration)
    upperBound = calculateCosts(district.houses, district.batteries)

    # Save initial configuration as best solution so far
    best = district
    best.save("Initial district")
    stop = 5000
    i = 0
    #district.houses.sort(key = lambda x: x.output, reverse = True)

    # Splice houselist with each step!
    length = len(district.houses) - 1
    while i < stop:
        # Randomly choose indexes for swaps
        #index = randint(0, 149)
        #index2 = randint(0, 149)
        # Take care that not the same is chosen
        #while index == index2:
        #    index = randint(0, 149)

        # Switch them as possible
        switch(district.houses[i % length], district.houses[(i % length) + 1])
        district.costs = calculateCosts(district.houses, district.batteries)

        # If costs are lower than keep it
        if district.costs < upperBound:
            print("!!!!!!HIT!!!!!!!")
            upperBound = district.costs
            district.save("Iteration" + str(i))
        # Switch back
        else:
            switch(district.houses[i % length], district.houses[(i % length) + 1])
        i += 1
        if i%length == 0:
            shuffle(district.houses)

def simulated(district):
    temperature = 100

    index = randint(0, 149)
    index2 = randint(0, 149)

    upperBound = calculateCosts(district.houses, district.batteries)

    switch(district.houses[index1],district.houses[index2])
    district.costs = calculateCosts(district.houses,district.batteries)
