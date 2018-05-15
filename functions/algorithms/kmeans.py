def kmeans(district):
    for b in district.batteries:
        meanLocation = (0,0)
        for h in b.connectedHouses:
            meanLocation[0] += h.location[0]
            meanLocation[1] += h.location[1]
