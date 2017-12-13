
import csv
import math
from collections import Counter
from _utils import *

params = {
	'threshold' : 0.07
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
	def __init__(self, delimiter, datadump):
		self.delim = delimiter
		self.datad = datadump
		self.rows = None
		self.categories = Counter()
		self.categories_words = Counter()
	def process(self):
		self.read_dump()
		self.count_categories()
		self.tokenize()
		self.tfidf()
	def read_dump(self):
		if not self.rows:
			with open(self.datad, 'r') as c:
				reader = csv.reader(c, delimiter=self.delim, skipinitialspace=True)
				next(reader) # Skip header
				self.rows = [row for row in reader]
		return self.rows
	def count_categories(self):
		if (len(self.categories) > 0):
			return self.categories
		for row in self.rows[1:]:
			row[0] = row[0].lower()
			self.categories[row[0]] += 1
		return self.categories
	def tokenize(self):
		for row in self.rows:
			row[1] = tokenize(row[1])
	def tfidf(self):
		for i, row in enumerate(self.rows):
			# print("Top words in document {}".format(i + 1))
			scores = {word: tfidf(word, row[1], self.rows[1]) for word in row[1]}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			for word, score in sorted_words[:3]:
				if (score > params['threshold']):
					print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
