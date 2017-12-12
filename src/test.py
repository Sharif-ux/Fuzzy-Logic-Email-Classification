
from _utils import *
from _preprocessing import *

datadump_path = "res/klachtendumpgemeente.csv"
dumpreader = Dumpreader(datadump_path)

rows = dumpreader.get_rows()

print(len(dumpreader.rows))
