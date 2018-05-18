def kmeans(district):
    for b in district.batteries:
        meanLocation = [0,0]
        i = 0
        for h in b.connectedHouses:
            meanLocation[0] += h.location[0]
            meanLocation[1] += h.location[1]
            i += 1
        meanLocation[0] = round(meanLocation[0] / i - 1)
        meanLocation[1] = round(meanLocation[1] / i - 1)
        print(meanLocation)
        b.changeLocation(meanLocation)
    #district.disconnect()
    #district.connectGreedy()
    #district.connectUnconnected()
    district.calculateCosts()
