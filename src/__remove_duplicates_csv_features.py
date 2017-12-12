
from _utils import *

path = "res/features/*csv"

# Prompting user for safety
go = input("You're about to overwrite the feature list csv's in " + path
			+ "\nType 'GO' if that's what you'd like to do: ")

if (go != 'GO'):
	print("You failed to type GO, aborting.")
	sys.exit()

csvs = [fname for fname in glob.glob(path)]

for csv in csvs:
    rows = read_csv(csv)
    content = []
    for row in rows:
        content = content + row

    unique = list(set(content))

    generate_csv_from_array(csv, unique)

print("Done.")
