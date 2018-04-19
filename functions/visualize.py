import matplotlib.pyplot as plt

'''' visualisation method using matplotlib and location data from house/battery objects '''
def visualize(houses, batteries):
    fig, ax = plt.subplots()

    a = []
    b = []

    x = []
    y = []

    for house in houses:

        a.append(house.location[0])
        b.append(house.location[1])

    for battery in batteries:

        x.append(battery.location[0])
        y.append(battery.location[1])

    ax.plot(a, b, 'ro')
    ax.plot(x, y, 'b    o')
    ax.grid()
    ax.axis('equal')
    plt.show()
