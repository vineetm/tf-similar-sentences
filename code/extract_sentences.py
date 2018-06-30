import argparse
import logging
import re
import spacy

from gensim.corpora.wikicorpus import WikiCorpus

EMPH_P1 = re.compile(r'((\w+\s)+)?\'\'\'(-?\w+((\s\w+)+)?)\'\'\'')
EMPH_P2 = re.compile(r'((\w+\s)+)?\'\'(-?\w+((\s\w+)+)?)\'\'')

nlp = spacy.load('en', disable=['parser', 'tagger', 'ner'])
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dump')
    parser.add_argument('-text')
    return parser.parse_args()

IGNORE_STARTS=['{', *', #REDIRECT', '==']
def ignore_sentence(sentence):
    if not sentence:
        return True

    for ignore_start in IGNORE_STARTS:
        if sentence.startswith(ignore_start):
            return True

    return False


def tokenize_text(sentence, lower):
    return ' '.join([token.text.lower() if lower else token.text for token in nlp(sentence)])


def clean_sentence(sentence):
    sentence = re.sub(EMPH_P1, r'\3', sentence)
    sentence = re.sub(EMPH_P2, r'\3', sentence)
    return sentence


def tokenize_spacy(text, token_min_len=-1, token_max_len=-1, lower=True):
    #Spacy constraints
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