import matplotlib.pyplot as plt
import matplotlib.lines as lines

'''' visualisation method using matplotlib and location data from house/battery objects '''
def visualize(district, save = False, numIt = False):

    houses = district.houses
    batteries = district.batteries

    fig, ax = plt.subplots()
    numBat = len(batteries)
    colors = ["xkcd:reddish pink", "xkcd:bright yellow", "xkcd:light neon green", \
              "xkcd:light royal blue", "xkcd:off white"]
    batterymarkers = ['$0$', '$1$', '$2$', '$3$', '$4$']
    connections = [[] for _ in range(numBat * 2)]

    unconnectedx = []
    unconnectedy = []

    x = []
    y = []

    # display houses (with or without connection)
    for house in houses:
        if house.connection != "NOT CONNECTED!": # NOTE: the

            i = house.connection.id
            j = house.connection.id + numBat

            connections[i].append(house.location[0])
            connections[j].append(house.location[1])

        else:
            unconnectedx.append(house.location[0])
            unconnectedy.append(house.location[1])

            ax.plot(unconnectedx, unconnectedy, 'wx', markersize=10)

    for battery in batteries:

        x.append(battery.location[0])
        y.append(battery.location[1])

    # display links between houses and their batteries
    for i in range(0, numBat):
        ax.plot(connections[i], connections[i+numBat], color = colors[i], marker = 'o', linestyle = 'None')

        for j in range (0, len(connections[i])):

            edgeX = x[i]
            edgeY = connections[i+numBat][j]

            linex1 = [connections[i][j], edgeX]
            liney1 = [connections[i+numBat][j], edgeY]

            linex2 = [edgeX, x[i]]
            liney2 = [edgeY, y[i]]

            ax.add_line(lines.Line2D(linex1, liney1, color=colors[i], alpha=0.5))
            ax.add_line(lines.Line2D(linex2, liney2, color=colors[i], alpha=0.5))

    for i in range(len(x)):
        ax.plot(x[i], y[i], color = colors[i], marker = batterymarkers[i], markersize=15)

    # Dynamically name plots from a loop
    savenamve = "plotDistrict.png"
    if numIt:
        saveName = "plotDistrict" + numIt + ".png"

    ax.grid()
    ax.set_facecolor('xkcd:charcoal')
    ax.axis('equal')
    if save == True:
        plt.savefig(saveName, dpi=250)
    if save == False:
        plt.show()
