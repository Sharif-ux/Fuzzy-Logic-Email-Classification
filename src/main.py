

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
    path = "res/features/*.csv"

    # Clean, tokenize, and rate all emails
    ratings = prepare_ratings(path)

    # Create a fuzzy logic instance
    classifier = prepare_classifier(path)

    # Classify first email using the email ratings
    for email in [next(ratings) for _ in range(30)]:
        classifier.classify(list(email.values()))

def prepare_ratings(path):
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
    rater = Rater(path)
	# print(rater.rate_words(next(rows_iterator)))
	# print(rater.rate_email(next(rows_iterator)))
    return (rater.rate_email(email) for email in rows_iterator)

def prepare_classifier(path):
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

    # Inputs all look the same, |\/\/|, ranging inclusively from 0 to 1 for
    # each feature list.
    inputs = [
        [Input(os.path.basename(fname).split('.')[0], (0, 1), [
            TrapezoidalMF("low", 0, 0, 0, 0.5),
            TriangularMF("med", 0, 0.5, 1),
            TrapezoidalMF("high", 0.5, 1, 1, 1)
        ]) for fname in glob.glob(path)]
    ]

    # The outputs are the department and priority of the email.
    outputs = [
        Output("department", (0, 8), [
            TrapezoidalMF("overig", 0, 0, 0, 0.125),
            TriangularMF("basisinformatie", 0, 0.125, 0.25),
            TriangularMF("openbare ruimte", 0.125, 0.25, 0.375),
            TriangularMF("onderwijs, jeugd en zorg", 0.25, 0.375, 0.5),
            TriangularMF("stadsloket", 0.375, 0.5, 0.625),
            TriangularMF("parkeren", 0.5, 0.625, 0.85),
            TriangularMF("werk en inkomen", 0.625, 0.75, 0.875),
            TriangularMF("belastingen", 0.75, 0.875, 1),
            TrapezoidalMF("overlast", 0.875, 1, 1, 1)
        ]),
        Output("priority", (0, 1), [
            TrapezoidalMF("execution", 0, 0, 0, 0.5),
            TriangularMF("management", 0, 0.5, 1),
            TrapezoidalMF("political", 0.5, 1, 1, 1)
        ])
    ]

    # Rules
    rules = [

        Rule(1, ["", "", "", "", "", "", ""], "and", ["", ""]),
        Rule(2, ["", "", "", "", "", "", ""], "and", ["", ""]),

    ]

    # Creating classifier
    classifier = Classifier(inputs, outputs, rules)
    classifier.reason()
    return classifier

def prepare_results():
    print("TODO!")

# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv[-1])
