# tf-similar-sentences

#### Installation:
* Clone the repo:
    ```bash
    git clone https://github.com/vineetm/tf-similar-sentences.git
    cd tf-similar-sentences/
    ```
    
* [Install Anaconda](https://www.anaconda.com/download/#macos). Create a new environment. Feel free to replace `tf-wiki` with name of your choice.    
    ```bash
    conda create -n tf-wiki python=3.6
    ```
    
* Install dependencies    
    ``` bash
    source activate tf-wiki
    (tf-wiki) pip install -r requirements.txt
    python -m spacy download en
    ```

#### Get English Wikipedia corpus 
This requires 15G of diskspace, and took us 2 hours. Speeds could wary. Feel free to replace the XML with [another version](https://dumps.wikimedia.org/enwiki/). You should look for files ending in `pages-articles.xml.bz2`
    
```bash
cd code
(tf-wiki) chmod +x download_wiki.sh
(tf-wiki) ./download_wiki.sh
```

#### Extract Sentences 
We use [gensim.wikicorpus](https://radimrehurek.com/gensim/corpora/wikicorpus.html) to parse XML. We replace default tokenizer to return sentences.

This required us about 8 hours on a system with 8 cores. More cores should work faster!
```bash
(tf-wiki) python extract_sentences.py -dump enwiki-20180601-pages-articles.xml.bz2 -text wiki.sentences.txt 
```
This results in about 91M sentences
```bash
(tf-wiki) wc -l wiki.sentences.txt
(tf-wiki) 91686995 wiki.sentences.txt
```

Further, extract unique sentences. We get about 53M sentences
```bash
(tf-wiki) python uniq_sentences.py -sentences wiki.sentences.txt -uniq wiki.sentences.txt.uniq  
```
```bash
(tf-wiki) wc -l wiki.sentences.txt.uniq
(tf-wiki) 53464766 wiki.sentences.txt.uniq
```

#### Build Annoy Index
We use [Annoy Index](https://github.com/spotify/annoy) to index Wikipedia sentences. Note that this requires about 150GB of disk space and 120GB of RAM.
```bash
(tf-wiki) python build_annoy_index.py -sentences wiki.sentences.txt.uniq -ann wiki.annoy.index   
```
