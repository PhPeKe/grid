def kmeans(district, index = 0):
    for b in district.batteries:
        meanLocation = [0,0]
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        meanLocation[0] = round(meanLocation[0] / len(b.connectedHouses))
        meanLocation[1] = round(meanLocation[1] / len(b.connectedHouses))
        b.changeLocation(meanLocation)
    district.calculateCosts()
    district.disconnect
    district.connectGreedy(True)
    i = 0
    while (district.allConnected == False):
        district.disconnect()
        district.connectGreedy()
        i += 1
        if i > 100:
            print("NO SOLUTION WITHIN 100 ITERATIONS")

    district.calculateCosts()

    if index < 100:
        kmeans(district, index + 1)
