# Classes

### house.py
**House-object**
##### Attributes:
- Location
- Distance to nearest battery
- Output of the individual house
- Connection: Reference to the connected battery-object
- Possible connections: all possible connections

##### Methods:
- connectNearestBattery()
  - Connects to nearest battery if it fits into the capacity
- connectRandomBattery()
  - Connects to random battery


### battery.py
**Battery-object**
##### Attributes:
- Location
- maxCapacity: maximum capacity, is changed when type changes
- capacity: capacity, is changed when house connects
- Costs: costs, updated when type is changed
- connectedHouses: List of all currently connected houses
- totalDistance: total distance to all connected houses
- closestBattery
- closestBatteryDistance
- Type: type of battery (initiated as -1 when no type is used)

##### Methods:
- totalDistance()
  - Calculates total distance
- changeLocation()
  - Changes location of battery and resets distance in houses
- showConnections()
  - Prints all connections in a user-friendly way


### district.py
**District-object**
##### Attributes:
- Houses
- Batteries
- Costs: costs of the whole configuration
- disconnectedHouses: List of all disconnected houses
- nthChoiceHouses: List of all houses that couldnt be connected to the closest battery
- compare
- allConnected: Boolean that displays if all houses are connected)

##### Methods:
- connectRandom()
  - Connects all houses randomly
- connectGreedy()
  - connects all houses to the closest battery if possible
  - If random = true the order of houses to connect is randomized
- save()
  - Saves district as csv
- disconnect()
  - disconnects all houses from their batteries
- calculateCosts()
  - calculates and updates costs
- setClosestBattery()
  - finds and saves the closest battery for each battery
- hillclimber()
  - optimizes connections in a connected district
