# Fuzzy Logic Email Classification

<p align="center"><img width="240" src="https://i.imgur.com/BEJpU4k.png"></p>

### 1. Plan

Seperti namanya, mengklasifikasikan email menggunakan Fuzzy Logic System.
<a href="https://github.com/Menziess/Fuzzy-Logic-Email-Classification/blob/master/report/group_7_draftreport.pdf">
  <p align="center"><img width="625" src="https://i.imgur.com/HYQRXDK.jpg"></p>
</a>

1. Run ```python3 src/__data_preparation.py``` untuk memasukkan data dump untuk memastikan bahwa kata-kata yang diekstrak tidak menyusun kembali keseluruhan data dengan cara yang berlebihan, ekstrak kata-kata yang bermakna menggunakan pelatihan datadump setelah membersihkan dokumen, membuat daftar csv untuk setiap kategori, dan gabungan 'word_list 'untuk menyaring kata-kata yang tidak relevan dari email masukan.
2. Run ```python3 src/main.py``` untuk menjalankan aplikasi utama, yang mengklasifikasikan bagian dari datadump validasi.

### 2. Installation

Step untuk windows 10

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

Untuk mempersiapkan datadump tertentu:

    $ python3 src/data_preparation.py

Untuk menjalankan program utama:

    $ python3 src/main.py

Untuk menjalankan salah satu sprint yang menjelaskan langkah-langkah yang diambil:

    $ jupyter notebook
