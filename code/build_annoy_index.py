import argparse
from annoy import AnnoyIndex
import tensorflow as tf
import tensorflow_hub as hub
import time
import sys


def print_with_time(msg):
    print('{}: {}'.format(time.ctime(), msg))
    sys.stdout.flush()


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sentences')
    parser.add_argument('-ann')
    parser.add_argument('-batch_size', default=32, type=int)
    parser.add_argument('-num_trees', default=10, type=int)
    return parser.parse_args()


def build_index(embedding_fun, batch_size, sentences):
    ann = AnnoyIndex(512)
    batch_sentences = []
    batch_indexes = []
    last_indexed = 0
    num_batches = 0
    with tf.Session() as sess:
        sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
        with open('wiki.txt.uniq', 'r') as fr:
            for sindex, sentence in enumerate(fr):
                batch_sentences.append(sentence)
                batch_indexes.append(sindex)

                if len(batch_sentences) == batch_size:
                    context_embed = sess.run(embedding_fun, feed_dict={sentences: batch_sentences})
                    for index in batch_indexes:
                        ann.add_item(index, context_embed[index - last_indexed])
                        batch_sentences = []
                        batch_indexes = []
                    last_indexed += batch_size
                    if num_batches % 10000 == 0:
                        print_with_time('sindex: {} annoy_size: {}'.format(sindex, ann.get_n_items()))
                    num_batches += 1
            if batch_sentences:
                context_embed = sess.run(embedding_fun, feed_dict={sentences: batch_sentences})
                for index in batch_indexes:
                    ann.add_item(index, context_embed[index - last_indexed])
    return ann


def main():
    args = setup_args()
    print_with_time(args)

    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")
    sentences = tf.placeholder(dtype=tf.string, shape=[None])
    embedding_fun = embed(sentences)

    ann = build_index(embedding_fun, args.batch_size, sentences)
    ann.build(args.num_trees)
    ann.save(args.ann)


if __name__ == '__main__':
    main()