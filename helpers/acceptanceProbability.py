from math import exp

def acceptanceprobability(newCosts, currentCosts, temperature): # naar helpers
    if newCosts < currentCosts:
        return 1.0
    else:
        return exp((currentCosts - newCosts) / temperature)
