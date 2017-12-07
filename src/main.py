

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
    classifier.classify(list(next(ratings).values()))

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
    # Input variable: personal
    mfs_personal = [TrapezoidalMF("possible", -10, 0, 20, 40), TriangularMF("probable", 20, 50, 80), TrapezoidalMF("certain", 60, 80, 100, 120)]
    personal = Input("personal", (0, 100), mfs_personal)

    # Input variable: space
    mfs_space = [TrapezoidalMF("possible", -10, 0, 20, 40), TriangularMF("probable", 20, 50, 80), TrapezoidalMF("certain", 60, 80, 100, 120)]
    space = Input("space", (0, 100), mfs_space)

    # Input variable: financial
    mfs_financial = [TrapezoidalMF("possible", -10, 0, 20, 40), TriangularMF("probable", 20, 50, 80), TrapezoidalMF("certain", 60, 80, 100, 120)]
    financial = Input("financial", (0, 100), mfs_financial)

    # Input variable: traffic
    mfs_traffic = [TrapezoidalMF("possible", -10, 0, 20, 40), TriangularMF("probable", 20, 50, 80), TrapezoidalMF("certain", 60, 80, 100, 120)]
    traffic = Input("traffic", (0, 100), mfs_traffic)

    # Input variable: tax
    mfs_tax = [TrapezoidalMF("possible", -10, 0, 20, 40), TriangularMF("probable", 20, 50, 80), TrapezoidalMF("certain", 60, 80, 100, 120)]
    tax = Input("tax", (0, 100), mfs_tax)

    # Input variable: agitation
    mfs_agitation = [TriangularMF("neutral", 0, 20, 40), TriangularMF("dissatisfaction", 20, 50, 80), TriangularMF("anger", 20, 50, 80), TrapezoidalMF("turmoil", 60, 80, 100, 120)]
    agitation = Input("agitation", (0, 100), mfs_agitation)

    # Input variable: action
    mfs_action =[TrapezoidalMF("suggest", -10, 0, 20, 40), TriangularMF("needed", 20, 50, 80), TrapezoidalMF("now", 60, 80, 100, 120)]
    action = Input("action", (0, 100), mfs_action)

    # Output variable: department
    mfs_department = [TriangularMF("informatie", 0, 100, 200), TriangularMF("belastingen", 200, 300, 400), TriangularMF("parkeren", 400, 500, 600), TriangularMF("werkeninkomen", 600, 700, 800), TriangularMF("generalaffairs", 800, 900, 1000)]
    department = Output("department", (0, 1000), mfs_department)

    # Output variable: priority
    mfs_priority = [TriangularMF("execution", 0, 100, 200), TriangularMF("management", 200, 300, 400), TriangularMF("political", 400, 500, 600)]
    priority = Output("priority", (0, 1000), mfs_priority)

    # Inputs and Outputs
    inputs = [personal, space, financial, traffic, tax, agitation, action]
    outputs = [department, priority]

    # Rules
    rules = [
        Rule(1,
            ["", "", "", "", "certain", "", ""], "and",
            ["belastingen", "execution"]),
        Rule(2,
            ["certain", "", "certain", "", "", "", ""], "and",
            ["werkeninkomen", "execution"]),
        Rule(3,
            ["certain", "", "", "certain", "", "", ""], "and",
            ["parkeren", "execution"]),
        Rule(4,
            ["", "certain", "", "", "", "", ""], "and",
            ["generalaffairs", "execution"]),
        Rule(5,
            ["", "", "", "", "", "neutral", ""], "and",
            ["informatie", "execution"]),
        Rule(6,
            ["", "", "", "", "", "", "needed"], "and",
            ["informatie", "execution"]),
        Rule(7,
            ["", "", "", "", "", "", "now"], "and",
            ["generalaffairs", "management"]),
        Rule(8,
            ["", "", "", "", "", "turmoil", ""], "and",
            ["generalafffairs", "political"]),
        Rule(9,
            ["", "", "", "", "", "anger"], "and",
            ["generalaffairs", "management"])
        ]

    # Creating classifier
    classifier = Classifier(inputs, outputs, rules)
    classifier.reason()
    return classifier

def prepare_results():
    print("TODO!")

# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv[-1])
