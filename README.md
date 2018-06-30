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
    chmod +x download_wiki.sh
    ./download_wiki.sh
    ```