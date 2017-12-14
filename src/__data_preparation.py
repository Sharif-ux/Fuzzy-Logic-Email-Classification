
from __data_preparation.train_validation_splitter import *
from __data_preparation.categories_maker import *
from textblob import TextBlob as tb


dumps = [
	"res/klachtendumpgemeente.csv",
	"res/validationdump.csv",
	"res/traindump.csv",
]

# Splitting datadump into two 50% / 50% to prevent overfitting
Splitter(';', *dumps).split()

# Create lists of cleaned and filtered words for each category
# and a combined list for all distinct words of all categories
Corpus(';', dumps[-1]).process()
