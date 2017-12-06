
# Contains Filedump reading and processing classes

from _utils import *

# Paths
path_word_list = "res/features/word_list/word_list.csv"

class Dumpreader:
    """Reads an email dump from csv."""
    def __init__(self, path='./res/klachtendumpgemeente.csv', delimiter=';'):
        self.rows = read_csv(path, delimiter)
        self.categories = Counter()
        self.categories_words = Counter()
    def describe(self):
        print("Dumpinfo:\trows:",
            len(self.rows), "\tcategories:", len(self.categories))
        if (len(self.categories) > 0):
            for c in self.categories:
                print(c, ':', self.categories[c])
        if (len(self.categories_words) > 0):
            for c in self.categories:
                print(c, ':', self.categories_words[c].most_common()[:25], '\n')
    def count_categories(self):
        # If categories have already been processed, return them
        if (len(self.categories) > 0):
            return self.categories
        # Else, count and define categories
        self.rows[0][0] = 'Categorie'
        for row in self.rows[1:]:
            row[0] = row[0].lower()
            self.categories[row[0]] += 1
        return self.categories
    def count_categories_words(self):
        # If categories_words have already been processed, return them
        if (len(self.categories_words) > 0):
            return self.categories_words
        # Else, computationally expensive way to count words per category
        if (len(self.categories) <= 0):
            self.count_categories()
        for c in self.categories:
            self.categories_words[c] = Counter()
            print(c, ':', self.categories[c])
            for row in [row for row in self.rows[1:] if c == row[0]]:
                for col in [1,2,3]:
                    body = tokenize(row[col])
                    for word in body:
                        self.categories_words[c][word] += 1
        return self.categories_words
    def rows_iterator(self):
        return (tokenize(row[1]) for row in self.rows[1:])

class Rater:
    def __init__(self):
        self.path = "res/features/*.csv"
        self.word_list = read_csv(path_word_list)[0]
        self.feature_lists = [read_csv(fname)[0] for fname in glob.glob(self.path)]
    def corpus(self, email):
        words = [x for x in intersection(email, self.word_list)]
        return np.c_[np.unique(words, return_counts=True)]
    def rate_words(self, email):
        c = self.corpus(email)
        c_len = len(c)
        for f in self.feature_lists:
            c = np.c_[c, np.zeros(c_len)]
            for row in c:
                if (row[0] in f):
                    row[-1:] = round(int(row[1]) / c_len, 4)
        return c
    def rate_email(self, email):
        c = self.rate_words(email)
        ratings = dict()
        for i in range(len(self.feature_lists)):
            ratings[i] = min((c[:,i + 2].astype(np.float).sum()), 1.0)
        return ratings
