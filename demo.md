# Demo

## Intro (1:00 min)

1. Folder `src/` (30 s)

    > Our project contains two applications:
    > - one for preparing category lists used for rating emails
    > - second for classifying email using fuzzy logic, using ratings as inputs

1. Folders `/res` and `res/klachtendumpgemeente.csv` (30 s)

    The dump has 2 columns, a label and the body. The body contains
    all kinds of rubbish, as you can see there are still html breaks
    and stopwords in there, so we need to clean the data to make the
    desired feature word_lists.

## Part one(1:30 min)

1. Splitting `src/datapreparation.py`

    The first step is to split our data into a train and test set 70 /
    30, so we can test the performance of our classifier on the
    'unseen' test dataset.

1. Tf/idf `src/categories_maker.py`

    The second step is to create feature lists for each category,
    after cleaning, using tf/idf with a threshold of 0.2.

## Part two (2:30 min)

1. Procedure
   * Read the validation dump
   * Create rater
   * Read in category lists
   * Rate all the emails
   * Create inputs, outputs and rules
   * Create FL classifier
   * Start classifying rated emails

1. Running fuzzy logic classifier
    `src/main.py`

1. Show tokenize() method
