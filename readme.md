# Fuzzy Logic Email Classification

<p align="center"><img width="240" src="https://i.imgur.com/BEJpU4k.png"></p>

### 1. Plan

As the name suggests, classifies emails using a Fuzzy Logic System.

<a href="https://github.com/Menziess/Fuzzy-Logic-Email-Classification/blob/master/report/group_7_draftreport.pdf">
  <p align="center"><img width="625" src="https://i.imgur.com/HYQRXDK.jpg"></p>
</a>

### 2. Installation

This step only on Windows 10:

- Install Windows subsystem for Linux
- Install Ubuntu from the store

Both Ubuntu and Windows subsystem for Linux:

- Run bash
- Install git - ```sudo apt-get install git```
- Install pip3 - ```sudo apt-get install python3-pip3```
- Install many_stop_words - ```sudo pip3 install many_stop_words```
- Install pandas - ```sudo pip3 install pandas```
- Install numpy - ```sudo pip3 install numpy```
- Install nltk - ```sudo pip3 install nltk```

### 3. Run

Cloning the project:

    $ git clone git@github.com:Menziess/Fuzzy-Logic-Email-Classification.git
    $ cd Fuzzy-Logic-Email-Classification

To run the main program:

    $ python3 src/main.py

To run one of the sprints describing the steps taken:

    $ jupyter notebook

Run additional scripts for data processing:

    $ python3 src/__print_dump_lengths.py
    $ python3 src/__train_validation_maker.py
    $ python3 src/__categories_maker.py
    $ python3 src/__word_list_maker.py
    $ python3 src/__remove_duplicates_csv_features.py

