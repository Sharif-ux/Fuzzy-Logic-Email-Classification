
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
    """
    Tokenizer.

    Converts plain text to array of tokens.

    Parameters
    ----------
    body : str
        Plain text that is to be cleaned and tokenized.

    Returns
    -------
    List
        A cleaned list of words.

    """
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
    """
    Plain text reader.

    Reads and cleans a text file located at filepath.

    Parameters
    ----------
    filepath : string
        Location of the file.

    Returns
    -------
    List
        A cleaned list of words.

    """
    with open(filepath, 'r') as file:
        body = file.read()
    return tokenize(body)

def read_csv(filepath, delimiter=','):
    """
    Csv reader.

    Reads csv file.

    Parameters
    ----------
    filepath : str
        Location of the file.
    delimiter : str
        Delimiter character, separating values.

    Returns
    -------
    List
        Containing a list of words for each row.

    """
    with open(filepath, 'r') as c:
        return [row for row in csv.reader(c, delimiter=delimiter,
            skipinitialspace=True)]

def generate_csv_from_array(filename, array):
    """
    Csv from array.

    Writes array to csv file.

    Parameters
    ----------
    filename : str
        Location to write file to.
    array : List
        Array that needs to be written.

    """
    with open(filename + ".csv", 'w', newline='') as c:
        writer = csv.writer(c, delimiter=',')
        writer.writerow(array)

def intersection(array1, array2):
    """
    Intersection.

    Intersects two Lists, resulting in values that reside in both lists.

    Parameters
    ----------
    array1 : List
        First List.
    array2 : List
        Second List.

    Returns
    -------
    List
        Containing values that reside in both lists.

    """
    return (i for i in array1 if i in array2)
