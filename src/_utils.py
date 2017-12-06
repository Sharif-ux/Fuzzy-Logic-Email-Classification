
# Contains utility functions and imports

import sys
import csv
import glob
import nltk
import string
import pandas as pd
import numpy as np

# nltk.download('punkt')
# nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import Counter

def tokenize(body):
    tokens = word_tokenize(body)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('dutch'))
    words = [w for w in words if not w in stop_words]
#     stemmer = SnowballStemmer("dutch")
#     words = [stemmer.stem(word) for word in words]
    return words

def read_txt(filepath):
    with open(filepath, 'r') as file:
        body = file.read()
    return tokenize(body)

def read_csv(filepath, delimiter=','):
    with open(filepath, 'r') as c:
        return [row for row in csv.reader(c, delimiter=delimiter,
            skipinitialspace=True)]

def generate_csv_from_array(filename, array):
    with open(filename + ".csv", 'w', newline='') as c:
        writer = csv.writer(c, delimiter=',')
        writer.writerow(array)

def intersection(array1, array2):
    """Returns a generator, use next(generator)"""
    return (i for i in array1 if i in array2)
