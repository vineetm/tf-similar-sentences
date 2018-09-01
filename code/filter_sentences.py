import argparse
import tensorflow as tf

logging = tf.logging
logging.set_verbosity(logging.INFO)

IGNORE_START = set('= * - ? } # : | colspan= align= ( alignbars style= − rowspan= ( _ ;'.split())

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sentences')
    parser.add_argument('-filtered')
    return parser.parse_args()


def filter_sentence(sentence):
    sentence = sentence.strip()
    if not sentence:
        return True
    words = sentence.split()
    if len(words) == 1:
        return True

    for ignore_start in IGNORE_START:
        if sentence.startswith(ignore_start):
            return True
    return False


def main():
    args = setup_args()
    logging.info(args)

    with open(args.sentences) as fr, open(args.filtered, 'w') as fw:
        for index, sentence in enumerate(fr):
            if filter_sentence(sentence):
                continue
            fw.write(f'{sentence}')
            if index % 5000000 == 0:
                logging.info(f'Done: {index}')

if __name__ == '__main__':
    main()