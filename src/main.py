

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
    features_path = "../res/features/*.csv"

    # Clean, tokenize, and rate all emails
    feature_lists, email_ratings = prepare_ratings(features_path)

    # Create a fuzzy logic instance
    classifier = prepare_classifier(feature_lists)

    # List of possible outputs
    classes = ["Overig", "Basisinformatie", "Openbare ruimte", "Onderwijs, jeugd en zorg", "Stadsloket", "Parkeren", "Werk en inkomen",
        "Belastingen", "Overlast"]

    result_printer = ResultPrinter(classes)

    # Classify first email using the email rating
    for (dept, email, rating) in [next(email_ratings) for _ in range(10)]:
        classification = classifier.classify(dept, email, list(rating.values()))
        result_printer.print(classification)

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
    rows = dumpreader.get_rows()
    rater = Rater(path)
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
            TriangularMF("med", 0.2, 0.5, 0.8),
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
        #     TrapezoidalMF("execution", 1, 2, 2, 2),
        # ])

    ]

    # Rules are alphabetically ordered
    # We have 7 inputs, with 3 membership functions
    # So we have a gigantic amount of possibilities..
    rules = [

        # Moet alle overige opties opvangen
        Rule(1, ["", "", "", "", "", "", ""],
            "and", ["overig"]),

        # Geen features
        Rule(2, ["", "", "", "", "", "", ""],
            "and", ["basisinformatie"]),

        # Geen features
        Rule(3, ["", "", "", "", "", "", ""],
            "and", ["openbare ruimte"]),
        Rule(4, ["", "", "", "", "", "", ""],
            "and", ["openbare ruimte"]),

        # Helemaal geen features
        Rule(5, ["", "", "", "", "", "", ""],
            "and", ["onderwijs, jeugd en zorg"]),

        # No possible features
        Rule(6, ["", "", "", "", "", "", ""],
            "and", ["stadsloket"]),

        # 3e "financial" en laatset "traffic"
        Rule(7, ["", "", "med", "", "", "", "high"],
            "and", ["parkeren"]),
        Rule(8, ["", "", "high", "", "", "", "high"],
            "and", ["parkeren"]),

        # 3e "financial" 4e "personal"
        Rule(9, ["", "", "high", "high", "", "", ""],
            "and", ["werk en inkomen"]),
        Rule(10, ["", "", "med", "high", "", "", ""],
            "and", ["werk en inkomen"]),

        # 2e "agitation", 3e "financial" 6e "tax"
        Rule(11, ["", "low", "high", "", "", "high", ""],
            "and", ["belastingen"]),
        Rule(12, ["", "med", "high", "", "", "high", ""],
            "and", ["belastingen"]),
        Rule(13, ["", "high", "high", "", "", "high", ""],
            "and", ["belastingen"]),
        Rule(14, ["", "high", "high", "", "", "low", ""],
            "and", ["belastingen"]),
        Rule(15, ["", "high", "high", "", "", "med", ""],
            "and", ["belastingen"]),
        Rule(16, ["", "high", "low", "", "", "high", ""],
            "and", ["belastingen"]),
        Rule(17, ["", "high", "med", "", "", "high", ""],
            "and", ["belastingen"]),

        # 4e "personal" 5e "space"
        Rule(18, ["", "", "", "med", "high", "", ""],
            "and", ["overlast"]),
        Rule(19, ["", "", "", "low", "high", "", ""],
            "and", ["overlast"]),
        Rule(20, ["", "", "", "high", "med", "", ""],
            "and", ["overlast"]),
        Rule(21, ["", "", "", "high", "low", "", ""],
            "and", ["overlast"]),
        Rule(22, ["", "", "", "high", "high", "", ""],
            "and", ["overlast"]),
    ]

    # Creating classifier
    classifier = Classifier(inputs, outputs, rules)
    classifier.reason()
    return classifier

class ResultPrinter:
    """
    Result Printer.

    Prints a classification object.
    """
    def __init__(self, classes):
        self.classes = classes
        print("%15s / %15s / %1s" % ("LABEL", "CLASS", "FEATURES"))
    def print(self, classification):
        print(
            "%15s / %15s / %20s" %
            (classification['label'],
            self.classes[classification['class']['department']],
            classification['ratings'])
        )

# Calls main method and passes first argument
if __name__ =='__main__': main(sys.argv)
