

# Importing our utilities
from _utils import *
from _fuzzy import *
from _preprocessing import *

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
    # Clean, tokenize, and rate all emails
    ratings = prepare_ratings()

    # Create a fuzzy logic instance
    classifier = prepare_classifier()

    # Classify first email using the email ratings
    classifier.classify(next(ratings))

def prepare_ratings():
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

def prepare_classifier():
    """
    Classifier.

    Instance of a Classifier object that is able to classify emails by
    using the email feature vector as inputs.

    Returns
    -------
    Classifier
        Instance of a Classifier object that is able to classify emails by
        using the email feature vector as inputs.

    """
    return Classifier()

def prepare_results():
    print("TODO!")

# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv[-1])
