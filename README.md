# grid
In a future world houses all have solar panels that produce energy. This energy has to be stored in batteries and for this batteries have to be placed and connected to houses.

http://heuristieken.nl/wiki/index.php?title=SmartGrid

## Program usage
To run this program flags can be used.

    usage: main.py [-h] [-d {1,2,3}] [-p] [-s {ascending,descending,random}]
                   [-m {greedy,random}] [-sv {csv,verbose}] [-k KMEANSIT]

    optional arguments:
      -h, --help            show this help message and exit
      -d {1,2,3}, --district {1,2,3}
                            Specify the number of the district (1, 2, 3)
      -p, --plot            Flag if plots should be made
      -s {ascending,descending,random}, --sort {ascending,descending,random}
                            Sort houses before connecting to specify which house
                            should be connected first (ascending, descending,
                            random)
      -m {greedy,random}, --method {greedy,random}
                            Specify the method of initially assigning houses to
                            batteries (greedy, random)
      -sv {csv,verbose}, --save {csv,verbose}
                            Specify if and how districts should be saved
      -k, --kmeansIt        Number of iterations for kmeans

To run it on district 1 with random sorting houses and a greedy way of connecting them while producing a plot and saving the district to a csv file the user would have to run

    "main.py -d 1 -s random -m greedy -sv csv -p"


Here a step-for-step overview of what we did with the project:
### 1. Loading the data
  - from csv/txt files
  - into classes Battery and house
  - then adding all batteries and houses to class district
### 2. Connecting all houses to a battery:
  - Sorting houses by output (ascending, descending, random) to influence the order of which house is connected first/last
  - Connection options: greedy or random
     - Greedy: Each house is connected to its nearest battery (if there is enough capacity left)
      - Random: Each house is connected to a random battery
  - If not all houses could be connected a Hill-climbing algorithm switches houses around to make room for unconnected houses until every house is connected
### 3. Optimizing connections:
- Given a connected district a Hill-Climber is switching houses to minimize cable length
### 4. Moving batteries:
- Given an optimized district batteries are moved to the center of all houses that they are connected to to further minimize cable length
