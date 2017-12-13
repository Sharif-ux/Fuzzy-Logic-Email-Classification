
from _utils import *
from _preprocessing import *

dumps = [
	"res/klachtendumpgemeente.csv",
	# "res/validationdump.csv",
	# "res/traindump.csv"
]

for dump in dumps:
	dumpreader = Dumpreader(dump)
	dumpreader.count_categories_words()
	dumpreader.describe()
