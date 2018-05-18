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
    return parser.parse_args()
