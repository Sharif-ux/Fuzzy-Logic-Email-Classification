
import os
import csv
import math
from collections import Counter
from __data_preparation.utils import *

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
		self.params = params
		self.rows = None
		self.categories = None
	def process(self):
		self.read_dump()
		self.dist_categories()
		self.tokenize()
		self.filter_categories()
	def read_dump(self):
		if not self.rows:
			with open(self.params['traindump'], 'r') as c:
				reader = csv.reader(c,
					delimiter=self.params['delimiter'],
					skipinitialspace=True)
				next(reader) # Skip header
				self.rows = [row for row in reader]
		return self.rows
	def dist_categories(self):
		self.categories = list(set([row[0] for row in self.rows]))
	def tokenize(self):
		for row in self.rows:
			row[1] = tokenize(row[1])
	def filter_categories(self):
		if not os.path.exists(self.params['categories_path']):
			os.makedirs(self.params['categories_path'])
		if not os.path.exists(self.params['word_list_path']):
			os.makedirs(self.params['word_list_path'])
		word_list = []
		common_word_list = []
		for category in self.categories:
			print("Category:", category, "threshold:", self.params['threshold'])
			rows = [row for row in self.rows if category == row[0]]
			favorite_words = set(self.tfidf(rows))
			print(category + ":", len(favorite_words))
			word_list += favorite_words
			common_word_list = intersection(common_word_list, favorite_words)
			generate_csv_from_array(self.params['categories_path'] + category.lower() + ".csv", favorite_words)
		generate_csv_from_array(
			self.params['word_list_path'] + "word_list.csv",
			set([x for x in word_list if x not in common_word_list]))
	def tfidf(self, rows):
		favorite_words = []
		for i, row in enumerate(rows):
			scores = {word: tfidf(word, row[1], [r[1] for r in self.rows]) for word in row[1]}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			for word, score in sorted_words:
				if (score > self.params['threshold']):
					print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
					favorite_words.append(word)
		return favorite_words
