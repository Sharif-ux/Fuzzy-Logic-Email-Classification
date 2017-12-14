
from _utils import *
from _preprocessing import *

dumps = [
	"res/klachtendumpgemeente.csv",
	# "res/validationdump.csv",
	# "res/traindump.csv"
]

for dump in dumps:
	Dumpreader(dump).count_categories_words().describe()
