# grid
Renewable energy is getting more and more important. In a (hopefully) not too distant future most houses will have solar panels that produce energy. The surplus energy then is fed into the grid and saved in batteries so it can be used when the sun is not shining. But because we live in a world where everything costs money the length of the cables should be optimized to save money.

For more information about the case visit:
http://heuristieken.nl/wiki/index.php?title=SmartGrid

### The assignment was split into four parts:
1. Connecting all houses to a battery in all districts
2. Optimizing the connections
3. Moving the batteries to optimize costs
4. Placing different kinds of batteries with different price/capacity ratios


## Program usage
To run this program flags can be used.

    usage: main.py [-h] [-d {1,2,3}] [-p] [-s {ascending,descending,random}]
                   [-m {greedy,random}] [-sv {csv,verbose}] [-k KMEANSIT]
                   [-pt {a,b,c,d}]

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

      -k, --kmeansIt	Number of iterations for kmeans

      -pt {a,b,c,d}, --part {a,b,c,d}
                            Specifies until which part of the assignment the case
                            should be solved


To run it on district 1 completely with random sorting houses and a greedy way of connecting them while producing a plot and saving the district to a csv file the user would have to run

    "main.py -d 1 -s random -m greedy -sv csv -p -pt d"


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
### 5. Placing different kind of batteries
- Starting point is a set of the smallest kind of batteries possible. These are then connected to the grid, kmeans is used to minimize the costs of the battery configurations. Then the two batteries who are closest together join in one larger battery. This repeats in several iterations.
