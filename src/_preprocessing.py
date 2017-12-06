
# Contains Filedump reading and processing classes

from _utils   import *

# Read all emails
rows = read_csv('./res/klachtendumpgemeente.csv', ';')


def corpus(email, word_list):
    words = [x for x in intersection(email, word_list)]
    return np.c_[np.unique(words, return_counts=True)]
# print(corpus(email, word_list)[:10])

def rate(corpus, feature_lists):
    c_len = len(corpus)
    c = corpus
    for f in feature_lists:
        c = np.c_[c, np.zeros(c_len)]
        for row in c:
            if (row[0] in f):
                row[-1:] = round(int(row[1]) / c_len, 4)
    return c
# rating = rate(
#     corpus(email, word_list),
#     [starts_with_c, starts_with_m] )
# print("RATING:\n", rating)


def email_rating(email, feature_lists):
    c = rate(corpus(email, word_list), feature_lists)
    ratings = dict()
    for i in range(len(feature_lists)):
        ratings[i] = min((c[:,i + 2].astype(np.float).sum()), 1.0)
    return ratings
# inputs = email_rating(email, [starts_with_c, starts_with_m])
# print(inputs)


# WARNING! Intensive computation (not very well optimized)
# It counts all possible relevant words for each category
def generate_feature_lists():
  category_words = Counter()
  categories = Counter()

  rows[0][0] = 'Categorie'
  for row in rows[1:]:
      row[0] = row[0].lower()
      categories[row[0]] += 1

  for c in categories:
      category_words[c] = Counter()
      print(c, ':', categories[c])
      for row in [row for row in rows[1:] if c == row[0]]:
          for col in [1,2,3]:
              body = tokenize(row[col])
              for word in body:
                  category_words[c][word] += 1
  return categories, category_words

categories, category_lists = generate_feature_lists()

# Most common words
for c in categories:
    print(c, category_lists[c].most_common()[:25], '\n')
