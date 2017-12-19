
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

		# Write header
		v.writerow(data[0])
		t.writerow(data[0])

		# Shuffle rest
		data = data[1:]
		random.shuffle(data)

		# Split data based on factor
		f = params['train_data_split_factor']
		train_data = data[:int((len(data)+1) * f)]
		valid_data = data[int(len(data)* f + 1):]

		# Write data to csv files
		[t.writerow(row) for row in train_data]
		[v.writerow(row) for row in valid_data]

		print("Original dump length:", len(data))
		print("Written", len(train_data), "rows to \"" + params['traindump']
			+ "\" and", len(valid_data), "rows to \"" + params['validdump']
			+ "\" used a factor of:", f)
