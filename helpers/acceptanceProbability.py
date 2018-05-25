from math import exp

def acceptanceprobability(newCosts, currentCosts, temperature):
    """Calculates acceptance probability for methods which use simulated annealing"""
    if newCosts < currentCosts:
        return 1.0
    else:
        return exp((currentCosts - newCosts) / temperature)
