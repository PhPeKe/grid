def prompt():
    # Ask User which wijk to use, force 1,2 or 3 as input
    district = input("Choose district: ")
    while district not in ["1","2","3"]:
        district = input("Choose district(1, 2 or 3): ")

    plot = input("Make plot?(y/n): " )
    while plot not in ["y","n"]:
        plot = input("Press y or n!")

    sort = input("Sort by output?(y/n): " )
    while sort not in ["y","n"]:
        sort = input("Press y or n!")

    if sort == "y":
        sort += input("Ascending or descending?(a/d): " )
        while sort not in ["ya","yd"]:
            sort = "y"
            sort += input("Press a or d!: ")
            print(sort)

    return district, plot, sort
