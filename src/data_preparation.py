
from __data_preparation.train_validation_splitter import *
from __data_preparation.categories_maker import *

# Dump requires three values: input dump path, validation dump path
# and train dump paths, in that particular order
params = {
	'threshold' : 0.1,
	'delimiter' : ';',
	'dumps' : [
		"res/klachtendumpgemeente.csv",
		"res/validationdump.csv",
		"res/traindump.csv",
	],
	# Currently creating union word_list in categories folder
	# instead of features folder
	'word_list_path' : "res/categories/word_list/",
	'categories_path' : "res/categories/",
	'features_path' : "res/features/",
}

# Prompting user for safety
while True:
	print("You're about to write/overwrite category list csv's in '"
		+ params['categories_path']
		+ "'.\nEnter a threshold above 0, if that's what you'd like to do: ")
	try:
		t = float(input("> "))
		params['threshold'] = t
		break
	except ValueError:
		print("Man, learn to type a number.")

# Splitting datadump into two 50% / 50% to prevent overfitting
Splitter(params['delimiter'],
		*params['dumps']).split()

# Create lists of cleaned and filtered words for each category
# and a combined list for all distinct words of all categories
Corpus(params).process()
