
import os
import csv
import math
from collections import Counter
from __data_preparation.utils import *

# tf = frequency of a term in a given document
# n_containing = number of documents containing word
# idf = natural log of number of rows divided by number of rows containing word
def tf(word, row):
    return row.count(word) / len(row)
def n_containing(word, rows):
    return sum(1 for row in rows if word in row)
def idf(word, rows):
    return math.log(len(rows) / (1 + n_containing(word, rows)))
def tfidf(word, row, rows):
    return tf(word, row) * idf(word, rows)


class Corpus:
	"""Designed to filter meaningfull words from a datadump and store
	the words in a csv file having a corresponding label"""
	def __init__(self, params):
		self.rows = None
		self.categories = None
		self.process(params)

	# Starts steps of creating category lists
	def process(self, params):
		self.read_dump(params)
		self.count_distinct_categories()
		self.tokenize()
		self.filter_categories(params)

	# Reads the train datadump
	def read_dump(self, params):
		with open(params['traindump'], 'r') as c:
			reader = csv.reader(c,
				delimiter=params['delimiter'],
				skipinitialspace=True)
			self.rows = [row for row in reader][1:]

	# Counts distinct categories
	def count_distinct_categories(self):
		self.categories = list(set([row[0] for row in self.rows]))

	# Tokenizes and cleans email bodies
	def tokenize(self):
		for row in self.rows:
			row[1] = tokenize(row[1])

	# Creates lists of words, per category, with tf/idf score above threshold
	def filter_categories(self, params):
		if not os.path.exists(params['categories_path']):
			os.makedirs(params['categories_path'])
		if not os.path.exists(params['word_list_path']):
			os.makedirs(params['word_list_path'])
		word_list = []
		common_word_list = []

		# After folders are created, start tf/idf
		print("Starting tf/idf process, this may take a while...")
		for category in self.categories:
			print("Category:", category, "- threshold:", params['threshold'])
			rows = [row for row in self.rows if category == row[0]]
			favorite_words = set(self.tfidf(rows, threshold=params['threshold'], verbose=params['verbose']))
			print(category + ":", len(favorite_words))
			word_list += favorite_words
			common_word_list = intersection(common_word_list, favorite_words)
			generate_csv_from_array(params['categories_path'] + category.lower() + ".csv", favorite_words)

		# Creates final word_list, a union set of all category lists
		generate_csv_from_array(
			params['word_list_path'] + "word_list.csv",
			set([x for x in word_list if x not in common_word_list]))

	# Extracts words with tf/idf score above threshold
	def tfidf(self, rows, threshold=0.2, verbose=False):
		favorite_words = []
		for i, row in enumerate(rows):
			scores = {word: tfidf(word, row[1], [r[1] for r in self.rows]) for word in row[1]}
			best_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			for word, score in best_words:
				if (score >= threshold):
					if (verbose):
						print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
					favorite_words.append(word)
		return favorite_words
