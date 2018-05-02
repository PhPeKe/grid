from functions.calculateCosts import calculateCosts
from functions.switch import switch

def hillclimber(nthChoiceHouse, batteries, houses):

    currentCosts = calculateCosts(houses, batteries)
    battery = nthChoiceHouse.possible_connections[0][0]
    capacity_d = nthChoiceHouse.output - battery.capacity

    batteryConnections = battery.connectedHouses
    batteryConnections.sort(key=lambda x: x.distance, reverse=True)

    for cHouse in batteryConnections:
        if (cHouse.output + battery.capacity) >= capacity_d:
            switch(nthChoiceHouse, cHouse)
            newCosts = calculateCosts(houses, batteries)
            if newCosts < currentCosts:
                return
            else:
                switch(nthChoiceHouse, cHouse)
            return



# 1.voor alle huizen die niet eerste keuze batterij hebben:
# 2.	hoeveel capaciteit moet er bij de eerste keus batterij worden vrijgemaakt?
# 3.	zoek een huis bij de eerste keus batterij, met verste kabelafstand naar batterij, om mee te switchen
# 4. 		kortere totale kabel afstand?
# 5.			nee:
# 6.			geen switch
# 7.			ja:
# 8.			maak je genoeg capaciteit vrij?
# 9.				nee:
# 10.				zoek een tweede batterij met de kortste afstand naar andere batterij
# 11.				terug naar regel 4
# 12.				ja:
# 13.				switch & door naar volgend huis
