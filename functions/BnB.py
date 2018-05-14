from functions.calculateCosts import calculateCosts
from functions.switch import switch
from random import randint, shuffle


def optimize(district):
    """
    Takes a solution where all houses are connected and then tries to
    optimize with bounds
    """
    # Set initial upper bound (cost of the current configuration)
    upperBound = district.costs

    # Save initial configuration as best solution so far
    district.save("Initial district")
    stop = int(input("Enter numer of iterations: "))
    sort = input("Sort houses?")
    if sort == "y":
        sort = input("output, distance or both?")

    if sort == "o":
        district.houses.sort(key = lambda x: x.output)

    if sort == "d":
        district.houses.sort(key = lambda x: x.distance)

    if sort == "b":
        for house in district.houses:
            house.score = house.distance + house.output

        district.houses.sort(key = lambda x: x.score)


    i = 0
    #district.houses.sort(key = lambda x: x.output, reverse = True)

    # Splice houselist with each step!
    length = len(district.houses) - 1
    while i < stop:
        # Switch them as possible
        switch(district.houses[i % length], district.houses[(i % length) + 1])
        district.calculateCosts()

        # If costs are lower than keep it
        if district.costs < upperBound:
            print("!!!!!!HIT!!!!!!!: ",str(i))
            print(upperBound, district.costs)
            # Adjust upper bound
            upperBound = district.costs
            district.save("Iteration" + str(i))
        # Switch back and recalculate costs
        elif district.costs > upperBound:
            switch(district.houses[i % length], district.houses[(i % length) + 1])
            district.calculateCosts()
        i += 1
        if i%length == 0:
            shuffle(district.houses)
    district.calculateCosts()
    return
"""
def simulated(district):
    temperature = 100

    index = randint(0, 149)
    index2 = randint(0, 149)

    upperBound = calculateCosts(district.houses, district.batteries)

    switch(district.houses[index1],district.houses[index2])
    district.costs = calculateCosts(district.houses,district.batteries)
"""
