from classes.classes import *
from functions.loadData import *

housePath = "data/wijk1_huizen.csv"
batteryPath = "data/wijk1_batterijen.txt"

houses, batteries = loadData(housePath, batteryPath)
