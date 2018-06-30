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

#### Runtime Query
An interactive session can be fired as follows:
```bash
(tf-wiki) python find_similar_sentence.py -sentences wiki.sentences.txt.uniq -ann wiki.annoy.index
```

#### Examples
`Input1`: The Japanese sample-return spacecraft Hayabusa2 arrives at the asteroid 162173 Ryugu.

`Output1`:
```
the extraterrestrial ship from deep space enters the solar system and abducts a boater on earth .
after a comet collides with the ship , dart and his crew discover a new planet beyond the orbit of pluto .
the crew are on an expedition on the mysterious planet krop tor , impossibly in orbit around a black hole .
hurtling on into deep space , jupiter 2 crash lands on an unknown planet .
first flyby of pluto , charon , nix , hydra , kerberos , and styx , first up - close images of pluto system , first images of pluto and charon 's surfaces , first spacecraft to explore the kuiper belt .
the fourth , and only , spaceship to return from mars holds an insane crew and a martian " furball " .
drax plans to fire it at earth from space .
voyager 2 sends back images of neptune and its system
young man floats in escape pod after spacecraft explodes in deep space .
crew returning from first manned moon expedition witnesses atomic war break out on earth .
```

`Input2`: Saudi Arabia lifts its ban on women driving.

`Output2:`
```
the campaign aims to ban saudi arabia from the olympics until it allows saudi arabian women to take part in sports .
in september 2017 , the saudi arabian government announced that women would receive the right to drive , effective june 2018 .
saudi arabia in 2015 .
furthermore , the saudis are blocking a proposed causeway project between qatar and the uae and a proposed gas pipeline project between qatar and kuwait , because of saudi objections , the kuwaitis are now turning to the iranians for gas .
saudi officials said that , if successful in qualifying , female competitors would be dressed " to preserve their dignity " .
in 2015 , al - waleed was criticised for offering to buy bentley cars for saudi fighter pilots involved in the saudi arabian - led intervention in yemen .
saudi arabia agreed to allow its women athletes to compete in the 2012 olympics for the first time , amidst speculation that the entire saudi team might have been disqualified on grounds of gender discrimination .
* * 280px defense of saudi arabia 1990–1991
after widespread rumors about saudi arabia going to purchase an entire atoll from maldives , saudi arabian embassy in maldives issued a statement against the rumors .
saudi royal family after welcoming the new king salman of saudi arabia , january 27 , 2015
```

`Input3`: Ice drilling allows scientists studying glaciers and ice sheets to gain access to what is beneath the ice

`Output3`:
```
ice melting on lake baikal - nasa earth observatory.jpg |spring ice melt underway on lake baikal , on 4 may : notice the ice - covered north , while much of the south already is ice - free .
the volcano protrudes from the west antarctic ice cap and is itself covered with ice in its summit area .
in addition to frozen water , mars ice caps also have frozen carbon dioxide , commonly known as dry ice .
sea ice at the north pole in 2006
a first chronology for the north greenland eemian ice drilling ( neem ) ice core .
the arctic is affected by current global warming , leading to arctic sea ice shrinkage , diminished ice in the greenland ice sheet , and arctic methane release as the permafrost thaws .
they proposed that changes in air circulation patterns have led to increased upwelling of warm , deep ocean water along the coast of antarctica and that this warm water has increased melting of floating ice shelves at the edge of the ice sheet .
greenland ice sheet
meanwhile , in the arctic , the frozen aurochs in an ice shelf start drifting into the ocean .
file : antarctic peninsula , the larsen ice shelf , and the sea ice covered waters around the region.jpg|clear view of the antarctic peninsula , the larsen ice shelf , and the sea ice covered waters around the region .
```