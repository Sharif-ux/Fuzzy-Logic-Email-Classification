
import os
import csv
import math
from collections import Counter
from _utils import *

params = {
	'threshold' : 0.2,
	'categories_path' : "res/categories/"
}

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
	def __init__(self, delimiter, datadump):
		self.delim = delimiter
		self.datad = datadump
		self.rows = None
		self.categories = None
	def process(self):
		self.read_dump()
		self.dist_categories()
		self.tokenize()
		self.filter_categories()
	def read_dump(self):
		if not self.rows:
			with open(self.datad, 'r') as c:
				reader = csv.reader(c, delimiter=self.delim, skipinitialspace=True)
				next(reader) # Skip header
				self.rows = [row for row in reader]
		return self.rows
	def dist_categories(self):
		self.categories = list(set([row[0] for row in self.rows]))
	def tokenize(self):
		for row in self.rows:
			row[1] = tokenize(row[1])
	def filter_categories(self):
		if not os.path.exists(params['categories_path']):
			os.makedirs(params['categories_path'])
		for category in self.categories:
			print("Category:", category, "threshold:", params['threshold'])
			rows = [row for row in self.rows if category == row[0]]
			favorite_words = self.tfidf(rows)
			generate_csv_from_array(params['categories_path'] + category.lower() + ".csv", favorite_words)

	def tfidf(self, rows):
		favorite_words = []
		for i, row in enumerate(rows):
			scores = {word: tfidf(word, row[1], [r[1] for r in rows]) for word in row[1]}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			for word, score in sorted_words[:3]:
				if (score > params['threshold']):
					print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
					favorite_words.append(word)
		return favorite_words




