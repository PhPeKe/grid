import matplotlib.pyplot as plt
import matplotlib.lines as lines

'''' visualisation method using matplotlib and location data from house/battery objects '''
def visualize(houses, batteries):

    fig, ax = plt.subplots()
    numBat = len(batteries)
    colors = ["red", "yellow", "green", "blue", "black"]

    connections = [[] for _ in range(numBat * 2)]

    unconnectedx = []
    unconnectedy = []

    x = []
    y = []

    # display houses (with or without connection)
    for house in houses:
        if house.connection != "NOT CONNECTED!": # NOTE: the
            print(house.connection)

            i = house.connection.id - 1
            j = house.connection.id + numBat - 1

            connections[i].append(house.location[0])
            connections[j].append(house.location[1])

        else:
            unconnectedx.append(house.location[0])
            unconnectedy.append(house.location[1])

            ax.plot(unconnectedx, unconnectedy, 'bx')

    for battery in batteries:

        x.append(battery.location[0])
        y.append(battery.location[1])

        ax.plot(x, y, 'bo')

    # display links between houses and their batteries
    for i in range(0, numBat):
        ax.plot(connections[i], connections[i+numBat], 'ro')

        for j in range (0, len(connections[i])):

            linex = [connections[i][j],x[i]]
            liney = [connections[i+numBat][j], y[i]]
            ax.add_line(lines.Line2D(linex, liney, color=colors[i], alpha=0.6))

    ax.grid()
    ax.axis('equal')
    plt.show()
