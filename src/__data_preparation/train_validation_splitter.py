
import random
from __data_preparation.utils import *

class Splitter:
	"""Splits given dataset into train and validation sets."""
	def __init__(self, params):
		self.split(params)
	def split(self, params):
		data = read_csv(params['datadump'], params['delimiter'])
		t = csv.writer(open(params['traindump'], 'w', newline=''),
			delimiter=params['delimiter'])
		v = csv.writer(open(params['validdump'], 'w', newline=''),
			delimiter=params['delimiter'])

		# Write header then shuffle
		v.writerow(data[0])
		t.writerow(data[0])
		random.shuffle(data[1:])

		f = params['train_data_factor']

		train_data = data[1:int((len(data)+1) * f)]
		valid_data = data[int(len(data)* f + 1):]

		[t.writerow(row) for row in train_data]
		[v.writerow(row) for row in valid_data]

		print("Original dump length:", len(data))
		print("Written", len(train_data), "rows to \"" + params['traindump']
			+ "\" and", len(valid_data), "rows to \"" + params['validdump']
			+ "\" used a factor of:", f)
