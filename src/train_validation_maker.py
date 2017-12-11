
from _utils import *
from _preprocessing import *

train = 'res/traindump'
valid = 'res/validationdump'

dumpreader = Dumpreader()
dumpreader.describe()

with open(train + ".csv", 'w', newline='') as t:
	with open(valid + ".csv", 'w', newline='') as v:
		twriter = csv.writer(t, delimiter=';')
		vwriter = csv.writer(v, delimiter=';')
		for i, row in enumerate(dumpreader.rows):
			if i % 2 == 0:
				twriter.writerow(row)
			else:
				vwriter.writerow(row)

print("Written to", train, "and", valid, ".")
