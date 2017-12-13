
from _utils import *

class Splitter:
	"""Splits given dataset into 50/50 train and validation sets."""
	def __init__(self, delimiter, datadumppath, validationpath, trainpath):
		self.delim = delimiter
		self.datad = datadumppath
		self.valid = validationpath
		self.train = trainpath
	def split(self):
		dump_rows = read_csv(self.datad, self.delim)
		with open(self.train + ".csv", 'w', newline='') as t:
			with open(self.valid + ".csv", 'w', newline='') as v:
				twriter = csv.writer(t, delimiter=self.delim)
				vwriter = csv.writer(v, delimiter=self.delim)
				tlen, vlen = 1, 1
				for i, row in enumerate(dump_rows):
					# Write head
					if i == 0:
						twriter.writerow(row)
						vwriter.writerow(row)
					elif i % 2 == 0:
						tlen += 1
						twriter.writerow(row)
					else:
						vlen += 1
						vwriter.writerow(row)

		print("Written", tlen, "rows to", self.train, "and",
			vlen, "rows to", self.valid)
