

# Importing our utilities
from _utils   import *
from _preprocessing  import *
# from _fuzzy   import *

def main(path):
	"""
    Main method.

    Collection of all steps to classify emails, some steps may be commented out
	because they are only usefull for creating feature lists, word lists.

    Parameters
    ----------
    path : string
        Path given as input argument when running main.py

    """
	ratings = preprocess_ratings()
	print(next(ratings))

def preprocess_ratings():
    """
    Preprocessor.

    Cleans, tokenizes, categorizes, and rates emails.

    Returns
    -------
    generator
        Containing a set for each email, each set containing the feature and
		it's calculated rating.

    """
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

