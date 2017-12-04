
import csv
import nltk
import string
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def tokenize(body):
    tokens = word_tokenize(body)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    porter = PorterStemmer()
    words = [porter.stem(word) for word in words]
    return words

def read_txt(filepath):
    with open(filepath, 'r') as file:
        body = t.read()
    return tokenize(body)

def read_csv(filepath):
    with open(filepath, 'r') as c:
        reader = csv.reader(c, delimiter=',')
        for row in reader:
            return row

def generate_csv_from_array(filename, array):
    with open("res/" + filename + ".csv", 'w', newline='') as c:
        writer = csv.writer(c, delimiter=',')
        writer.writerow(array)

def intersection(array1, array2):
    """Returns a generator, use next(generator)"""
    return (i for i in array1 if i in array2)
