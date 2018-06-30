import argparse

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sentences')
    parser.add_argument('-uniq')
    return parser.parse_args()


def main():
    args = setup_args()
    print(args)

    sentences = set()
    with open(args.sentences) as fr:
        for index, sentence in enumerate(fr):
            sentences.add(sentence.strip())
            if len(sentences) % 10000000 == 0:
                print('i: {} unique: {}'.format(index, len(sentences)))

    with open(args.uniq, 'w') as fw:
        for sentence in sentences:
            fw.write('{}\n'.format(sentence))


if __name__ == '__main__':
    main()
