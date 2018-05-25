import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--district",
                        help = "Specify the number of the district (1, 2, 3)",
                        choices = ["1","2","3"])
    parser.add_argument("-p","--plot",
                        help = "Flag if plots should be made",
                        action = "store_true")
    parser.add_argument("-s","--sort",
                        help = "Sort houses before connecting to specify which house should be connected first (ascending, descending, random)",
                        choices = ["ascending","descending","random"])
    parser.add_argument("-m","--method",
                        help = "Specify the method of initially assigning houses to batteries (greedy, random)",
                        choices = ["greedy","random"])
    parser.add_argument("-sv","--save",
                        help = "Specify if and how districts should be saved",
                        choices = ["csv","verbose"])
    parser.add_argument("-k","--kmeansIt",
                        help = "Number of iterations for kmeans",
                        type = int)
    parser.add_argument("-pt","--part",
                        help = "Specifies until which part of the assignment the case should be solved",
                        choices = ["a","b","c","d"])
    args = parser.parse_args()

    # Force valid input of required arguments
    if args.district == None:
        args.district = input("Choose district: ")
        while args.district not in ["1","2","3"]:
            args.district = input("Choose district(1, 2 or 3): ")

    if args.kmeansIt == None:
        args.kmeansIt = 10

    if args.method == None:
        args.method = input("Choose method: ")
        while args.method not in ["greedy","random"]:
            args.method = input("Choose method(\"greedy\" or \"random\"): ")

    return args
