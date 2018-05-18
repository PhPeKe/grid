def kmeans(district):
    for b in district.batteries:
        meanLocation = [0,0]
        for h in b.connectedHouses:
            meanLocation[0] = meanLocation[0] + h.location[0]
            meanLocation[1] = meanLocation[1] + h.location[1]
        meanLocation[0] = meanLocation[0] / len(b.connectedHouses)
        meanLocation[1] = meanLocation[1] / len(b.connectedHouses)
        b.changeLocation(meanLocation)
    #district.disconnect()
    #district.connectGreedy()
    #district.connectUnconnected()
    district.calculateCosts()
