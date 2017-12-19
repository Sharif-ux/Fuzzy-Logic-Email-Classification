
from __data_preparation.train_validation_splitter import *
from __data_preparation.categories_maker import *

# Dump requires three values: input dump path, validation dump path
# and train dump paths, in that particular order
# The 'threshold' determines wihch minimal tf/idf score is required
# for words to end up in the category lists
params = {
	'threshold' : 0.2,
	'verbose'	: True,
	'delimiter' : ';',
	'train_data_split_factor' : .70,

	'datadump' 	: "res/klachtendumpgemeente.csv",
	'validdump' : "res/validationdump.csv",
	'traindump' : "res/traindump.csv",

	# Currently creating union word_list in categories folder
	# instead of features folder
	'word_list_path' : "res/categories/word_list/",
	'categories_path' : "res/categories/",
	'features_path' : "res/features/",
}

# Splitting datadump into two lists to prevent overfitting
Splitter(params)

# Create lists of cleaned and filtered words for each category
# and a combined list for all distinct words of all categories
# Prompting user to prevent unwanted overwriting of categories
while True:
	print("You're about to write/overwrite category list csv's in \""
		+ params['categories_path']
		+ "\".\nEnter a threshold above 0, if that's what you'd like to do: ")
	try:
		t = float(input("> "))
		params['threshold'] = t
		break
	except ValueError:
		print("Man, learn to type a number.")

Corpus(params)
