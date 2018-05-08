def calculateCosts(houses, batteries):
    costs = 0
    for house in houses:
        if not house.distance == 1000:
            costs += house.distance * 9
    for battery in batteries:
        costs += battery.costs
    return costs
