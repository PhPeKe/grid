def prompt():
    # Ask User which wijk to use, force 1,2 or 3 as input
    wijk = input("Choose Wijk: ")
    while wijk not in ["1","2","3"]:
        wijk = input("Choose Wijk(1, 2 or 3): ")

    plot = input("Make plot?(y/n): " )
    while plot not in ["y","n"]:
        plot = input("Press y or n!")

    sort = input("Sort by output?(y/n): " )
    while sort not in ["y","n"]:
        sort = input("Press y or n!")

    return wijk, plot, sort
