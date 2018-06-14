import argparse
from gensim.corpora.wikicorpus import extract_pages, filter_wiki
from gensim.utils import any2unicode
import re
import spacy
import bz2
import logging

EMPH_P1 = re.compile(r'\'\'\'(\w+)\'\'\'')

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dump')
    parser.add_argument('-text')
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

    return False


def tokenize_text(sentence, nlp):
    doc = nlp(sentence)
    tokens = [token.text.lower() for token in doc]
    text = ' '.join(tokens)
    return text


def main():
    args = setup_args()
    logging.info(args)

    nlp = spacy.load('en', disable=['parser', 'tagger', 'ner'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    fw = open(args.text, 'w')
    num = 0
    for (title, text, pageid) in extract_pages(bz2.BZ2File(args.dump)):
        text = filter_wiki(text)
        text = any2unicode(text)
        doc = nlp(text)

        sentences = [sentence.string.strip() for sentence in doc.sents]
        sentences = [sentence for sentence in sentences if not ignore_sentence(sentence)]
        sentences = [re.sub(EMPH_P1, r'\1', sentence) for sentence in sentences]
        sentences = [tokenize_text(sentence, nlp) for sentence in sentences]

        for sentence in sentences:
            fw.write('{}\n'.format(sentence))

        if num % 10000 == 1:
            logging.info('Completed {} articles'.format(num))
        num += 1


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    main()