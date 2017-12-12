
from _utils import *
from _preprocessing import *

dumps = [
	"res/klachtendumpgemeente.csv",
	"res/validationdump.csv",
	"res/traindump.csv"
]

for dump in dumps:
	dumpreader = Dumpreader(dump)
	rows = dumpreader.get_rows()
	print(dump, "has", len(dumpreader.rows), "rows.")
