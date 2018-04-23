import matplotlib.pyplot as plt
import matplotlib.lines as lines

'''' visualisation method using matplotlib and location data from house/battery objects '''
def visualize(houses, batteries):
    fig, ax = plt.subplots()

    a = []
    b = []

    x = []
    y = []

    batt1X = []
    batt1Y = []

    batt2X = []
    batt2Y = []

    batt3X = []
    batt3Y = []

    batt4X = []
    batt4Y = []

    batt5X = []
    batt5Y = []

    for house in houses:
        print(house.connection.id)
        # dit moet nog even mooi met nested lists oid

        if(house.connection.id == 0):
            batt1X.append(house.location[0])
            batt1Y.append(house.location[1])
        elif(house.connection.id == 1):
            batt2X.append(house.location[0])
            batt2Y.append(house.location[1])
        elif (house.connection.id == 2):
            batt3X.append(house.location[0])
            batt3Y.append(house.location[1])
        elif (house.connection.id == 3):
            batt4X.append(house.location[0])
            batt4Y.append(house.location[1])
        elif (house.connection.id == 4):
            batt5X.append(house.location[0])
            batt5Y.append(house.location[1])


    for battery in batteries:

        x.append(battery.location[0])
        y.append(battery.location[1])

    #calculate edge


    ax.plot(batt1X, batt1Y, 'ro')
    ax.plot(batt2X, batt2Y, 'ro')
    ax.plot(batt3X, batt3Y, 'ro')
    ax.plot(batt4X, batt4Y, 'ro')
    ax.plot(batt5X, batt5Y, 'ro')

    for i in range (0, len(batt1Y)):
        linex = [batt1X[i],x[0]]
        liney = [batt1Y[i], y[0]]
        ax.add_line(lines.Line2D(linex, liney, color = 'red'))

    for i in range (0, len(batt2Y)):
        linex = [batt2X[i],x[1]]
        liney = [batt2Y[i], y[1]]
        ax.add_line(lines.Line2D(linex, liney, color = 'green'))

    for i in range (0, len(batt1Y)):
        linex = [batt3X[i],x[2]]
        liney = [batt3Y[i], y[2]]
        ax.add_line(lines.Line2D(linex, liney, color = 'blue'))

    for i in range (0, len(batt1Y)):
        linex = [batt4X[i],x[3]]
        liney = [batt4Y[i], y[3]]
        ax.add_line(lines.Line2D(linex, liney, color = 'yellow'))

    for i in range (0, len(batt1Y)):
        linex = [batt5X[i],x[4]]
        liney = [batt5Y[i], y[4]]
        ax.add_line(lines.Line2D(linex, liney, color = 'black'))

    ax.plot(x, y, 'bo')
    ax.grid()
    ax.axis('equal')
    plt.show()
