

# Importing our utilities
from _utils import *
from _fuzzy import *
from _preprocessing import *


def main(args):
    """
    Main method.

    Collection of all steps to classify emails, some steps may be commented out
    because they are only usefull for creating feature lists, word lists.

    Parameters
    ----------
    args : List
        Input arguments could be used in the future.

    """
    features_path = "res/features/*.csv"
    datadump_path = "res/klachtendumpgemeente.csv"

    # Clean, tokenize, and rate all emails
    feature_lists, email_ratings = prepare_ratings(features_path, datadump_path)

    # Create a fuzzy logic instance
    classifier = prepare_classifier(feature_lists)

    classes = ["Overig", "Basisinformatie", "Openbare Ruimte", "Onderwijs",
        "jeugd en zorg", "stadsloket", "parkeren", "werk en inkomen",
        "belastingen", "overlast"]

    # Classify first email using the email rating
    print("%15s / %15s" % ("ORIGINAL LABEL", "CLASSIFICATION"))
    for (dept, email, rating) in [next(email_ratings) for _ in range(10)]:
        # print(classifier.classify(dept, email, list(rating.values())))
        classification = classifier.classify(dept, email, list(rating.values()))
        print(
            "%15s / %15s" %
            (classification['label'],
            classes[classification['class']['department']])
        )

def prepare_ratings(features_path, datadump_path):
    """
    Preprocessor.

    Cleans, tokenizes, categorizes, and rates emails.

    Parameters
    -------
    features_path
        String containing the path to the folder containing feature csv's
    datadump_path
        String containing the path of the datadump csv

    Returns
    -------
    generator
        Containing a set for each email, each set containing the feature and
		it's calculated rating.

    """
    dumpreader = Dumpreader(datadump_path)
    rows = dumpreader.get_rows()
    rater = Rater(features_path)
    return rater.feature_lists, ((row[0], row[1], rater.rate_email(row[1])) for row in rows)

def prepare_classifier(feature_lists):
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

        Input(feature[0], (0, 1), [
            TrapezoidalMF("low", 0, 0, 0, 0.5),
            TriangularMF("med", 0, 0.5, 1),
            TrapezoidalMF("high", 0.5, 1, 1, 1)
        ]) for feature in feature_lists

    ]

    # The outputs are the department and priority of the email.
    outputs = [

        Output("department", (0, 8), [
            TrapezoidalMF("overig", 0, 0, 0, 1),
            TriangularMF("basisinformatie", 0, 1, 2),
            TriangularMF("openbare ruimte", 1, 2, 3),
            TriangularMF("onderwijs, jeugd en zorg", 2, 3, 4),
            TriangularMF("stadsloket", 3, 4, 5),
            TriangularMF("parkeren", 4, 5, 6),
            TriangularMF("werk en inkomen", 5, 6, 7),
            TriangularMF("belastingen", 6, 7, 8),
            TrapezoidalMF("overlast", 7, 8, 8, 8)
        ]),

        # Output("priority", (0, 2), [
        #     TrapezoidalMF("execution", 0, 0, 0, 1),
        #     TriangularMF("management", 0, 1, 2),
        #     TrapezoidalMF("political", 1, 2, 2, 2)
        # ])

    ]

    # Rules order: action agitation financial personal space tax traffic
	# note: action en agitation zijn alleen voor output "priority"

    rules = [

        Rule(1, ["", "", "high", "", "", ""],
            "and", ["belastingen"]),
    ]

    # Creating classifier
    classifier = Classifier(inputs, outputs, rules)
    classifier.reason()
    return classifier

def prepare_results():
    print("TODO!")

# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv)
