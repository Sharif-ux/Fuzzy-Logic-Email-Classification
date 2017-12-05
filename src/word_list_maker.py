
import sys
import glob
from utils import *

path = "res/features/*.csv"

# Prompting user for safety
go = input("You're about to overwrite the word_list.csv file in " + path
			+ "\nType 'GO' if that's what you'd like to do: ")

if (go != 'GO'):
	print("You failed to type GO, aborting.")
	sys.exit()

# Find all csv files in defined path to convert to word_list
word_list = []
for fname in glob.glob(path):
	word_list = word_list + read_csv(fname)

generate_csv_from_array("res/features/word_list/word_list", set(word_list))

print("Done.")
