
from _utils import *
from _preprocessing import *

# Using train set to create categories
dump_path = "res/traindump.csv"

dumpreader = Dumpreader(dump_path)
dumpreader.count_categories()
dumpreader.count_categories_words()
dumpreader.describe()

if not os.path.exists("res/categories"):
    os.makedirs("res/categories")

amount = 200
for c in dumpreader.categories:
	top_words = []
	for i in dumpreader.categories_words[c].most_common()[:amount]:
		top_words.append(i[0])

	generate_csv_from_array("res/categories/" + c, top_words)
