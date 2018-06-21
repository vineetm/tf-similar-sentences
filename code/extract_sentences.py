import argparse
from gensim.corpora.wikicorpus import extract_pages, filter_wiki, WikiCorpus
from gensim.utils import any2unicode
import re
import spacy
import bz2
import logging
import signal
from multiprocessing import Pool

EMPH_P1 = re.compile(r'((\w+\s)+)?\'\'\'(-?\w+((\s\w+)+)?)\'\'\'')
EMPH_P2 = re.compile(r'((\w+\s)+)?\'\'(-?\w+((\s\w+)+)?)\'\'')

nlp = spacy.load('en', disable=['parser', 'tagger', 'ner'])
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dump')
    parser.add_argument('-text')
    parser.add_argument('-t', default=4, type=int)
    return parser.parse_args()


def ignore_sentence(sentence):
    if not sentence:
        return True

    if sentence.startswith('#REDIRECT'):
        return True

    if sentence.startswith('=='):
        return True

    if sentence.startswith('*'):
        return True

    if sentence.startswith('{'):
        return True

    return False


def tokenize_text(sentence, lower):
    doc = nlp(sentence)
    tokens = [token.text.lower() if lower else token.text for token in doc]
    text = ' '.join(tokens)
    return text


def clean_sentence(sentence):
    sentence = re.sub(EMPH_P1, r'\3', sentence)
    sentence = re.sub(EMPH_P2, r'\3', sentence)
    return sentence


def tokenize_spacy(text, token_min_len=-1, token_max_len=-1, lower=True):
    #Spact constraints
    text = text[:990000]
    final_sentences = []
    try:
        doc = nlp(text)
        for sentence in doc.sents:
            sentence_text = sentence.string.strip()
            if ignore_sentence(sentence_text):
                continue
            sentence_text = clean_sentence(sentence_text)
            sentence_text = tokenize_text(sentence_text, lower)
            if sentence_text:
                final_sentences.append(sentence_text)

        return final_sentences
    except UnicodeEncodeError:
        return final_sentences


def main():
    args = setup_args()
    logging.info(args)

    fw = open(args.text, 'w')
    corpus = WikiCorpus(args.dump, dictionary={'a'}, tokenizer_func=tokenize_spacy)
    for index, sentences in enumerate(corpus.get_texts()):
        for sentence in sentences:
            fw.write('{}\n'.format(sentence))

        if index % 10000 == 0:
            logging.info('Done Article: {}'.format(index))

    return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    main()