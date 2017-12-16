
def main():

	# Paramters to easily tune stuff
	params = {

		'limit'		: 5,
		'verbosity'	: False,
		'defuz' 	: "centroid",

		'delimiter' : ';',

		'datadump' 	: "res/klachtendumpgemeente.csv",
		'validdump' : "res/validationdump.csv",
		'traindump' : "res/traindump.csv",
		'features' 	: "res/categories/*.csv",
		'word_list' : "res/categories/word_list/word_list.csv",

	}

	# Read validation data
	dump = read_csv(params['validdump'],
					params['delimiter'])

	# Create rate object that creates
	# feature vectors for all emails
	rater =   Rater(params['features'],
					params['word_list'])

	# Lists with features used by the
	# rater object to rate the emails
	feature_lists = rater.feature_lists

	# Rows and rated generators to iterate
	# through rated and non-rated emails
	rows = ((row[0], tokenize(row[1])) for row in dump[1:])
	rated = ((row[0], row[1], rater.rate_email(row[1])) for row in rows)

	# Inputs for the Fuzzy Logic System
	inputs = [

		Input(feature[0], (0, 1), [
			TrapezoidalMF("low", 0, 0, 0, 0.5),
			TriangularMF("med", 0, 0.5, 1),
			TrapezoidalMF("high", 0.5, 1, 1, 1)
		]) for feature in feature_lists

	]

	# Outputs for the Fuzzy Logic System
	outputs = [

		Output(feature[0], (0, 1), [
			TrapezoidalMF("low", 0, 0, 0, 0.5),
			TriangularMF("med", 0, 0.5, 1),
			TrapezoidalMF("high", 0.5, 1, 1, 1)
		]) for feature in feature_lists

	]

	# Rules for the Fuzzy Logic System
	rules = [

		Rule(1, ["high", "", "", ""],
			"and", ["high", "", "", ""]),
		Rule(2, ["med", "", "", ""],
			"and", ["med", "", "", ""]),
		Rule(3, ["low", "", "", ""],
			"and", ["low", "", "", ""]),
		Rule(4, ["", "", "high", ""],
			"and", ["", "", "high", ""]),
		Rule(5, ["", "", "med", ""],
			"and", ["", "", "med", ""]),
		Rule(6, ["", "", "low", ""],
			"and", ["", "", "low", ""]),
		Rule(7, ["", "", "", "high"],
			"and", ["", "", "", "high"]),
		Rule(8, ["", "", "", "med"],
			"and", ["", "", "", "med"]),
		Rule(9, ["", "", "", "low"],
			"and", ["", "", "", "low"]),
		Rule(10, ["", "high", "", ""],
			"and", ["", "high", "", ""]),
		Rule(11, ["", "med", "", ""],
			"and", ["", "med", "", ""]),
		Rule(12, ["", "low", "", ""],
			"and", ["", "low", "", ""]),

		# Catches empties
		Rule(13, ["low", "low", "low", "low"],
			"and", ["high", "", "", ""]),

	]

	# Fuzzy Logic Classifier
	classifier = Classifier(
		inputs, outputs,
		rules, params['defuz']
	)

	# Analyzes entire or parts of a classification
	# of the validation dataset
	analyzer = Analyzer()

	# analyzer.rate_all(rated, classifier, verbosity=True)
	analyzer.start(
		rated, classifier,
		limit=params['limit'], verbosity=params['verbosity']
	)

# Cleans plain text into arrays of words
def tokenize(body):
	tokens = word_tokenize(body)
	tokens = [w.lower() for w in tokens]
	tokens = [w for w in tokens if len(w) > 2]
	table = str.maketrans('', '', string.punctuation)
	stripped = [w.translate(table) for w in tokens]
	words = [word for word in stripped if word.isalpha()]
	stop_words = list(get_stop_words('nl'))
	nltk_words = list(stopwords.words('dutch'))
	stop_words.extend(nltk_words)
	words = [w for w in words if not w in stop_words]
	stemmer = SnowballStemmer("dutch")
	words = [stemmer.stem(word) for word in words]
	return words

# Reads comma separated file
def read_csv(filepath, delimiter=','):
	with open(filepath, 'r') as c:
		return [row for row in csv.reader(c, delimiter=delimiter,
			skipinitialspace=True)]

# Compares arrays of words and calculates a score
class Rater:
	def __init__(self, features, word_list):
		self.path = features
		self.word_list = read_csv(word_list)[0]
		self.feature_lists = [
			(os.path.basename(fname).split('.')[0],
			read_csv(fname)[0])
			for fname in glob.glob(self.path)]
		self.feature_lists.sort(key=lambda tup: tup[0])
	def corpus(self, email):
		words = [w for w in email if w in self.word_list]
		return np.c_[np.unique(words, return_counts=True)]
	def rate_words(self, email):
		c = self.corpus(email)
		c_len = len(c)
		for n, f in self.feature_lists:
			c = np.c_[c, np.zeros(c_len)]
			for row in c:
				if (row[0] in f):
					row[-1:] = int(row[1]) / c_len
		return c
	def rate_email(self, email):
		c = self.rate_words(email)
		ratings = dict()
		for i, feature in enumerate(self.feature_lists):
			agg = min(c[:,i + 2].astype(np.float).sum(), 1.0)
			ratings[feature[0]] = float(format(agg, '.2f'))
		return ratings

# Classifies one or bulks of emails
class Analyzer:
	def __init__(self):
		self.format = "%20s | %20s | %1s"
		self.trunc = lambda x: (x[:18] + '..') if len(x) > 18 else x
		self.best = lambda c: max(c, key=lambda k: c[k])
	def print(self, classification, verbosity):
		print(
			self.format %
			(
				self.trunc(classification['label'].lower()),
				self.trunc(self.best(classification['class'])),
				classification['ratings'] if (verbosity) else classification['feature_list']
			)
		)
	def start(self, rated, classifier, limit=None, verbosity=False):
		print(self.format % ("LABEL", "CLASS", "RATING"))
		for i, email in enumerate(rated):
			c = classifier.classify(email)
			self.print(c, verbosity)
			if i >= limit:
				break

# Imports hidden at the bottom
import os
import csv
import glob
import nltk
import string

nltk.download('punkt')
nltk.download('stopwords')

from many_stop_words import get_stop_words
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from __fuzzy_logic.classifier import *

# Calls main method
if __name__ =='__main__':
	main()
