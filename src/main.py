

# Importing our utilities
from _utils   import *
from _preprocessing  import *
# from _fuzzy   import *


def main(path):
	"""Main method."""
	ratings = preprocess_ratings()
	print(next(ratings))


def preprocess_ratings():
	"""Reads, cleans, processes and rates email dump."""
	dumpreader = Dumpreader()
	# dumpreader.count_categories()
	# dumpreader.count_categories_words()
	# dumpreader.describe()
	rows_iterator = dumpreader.rows_iterator()
	# print(next(rows_iterator))
	rater = Rater()
	# print(rater.rate_words(next(rows_iterator)))
	# print(rater.rate_email(next(rows_iterator)))
	return (rater.rate_email(email) for email in rows_iterator)




# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv[-1])

