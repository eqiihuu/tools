from sklearn.cluster import KMeans
import argparse

import file_io


def word_cluster(file_path, n_clusters=500):
    print('Loading data ...')
    words, vectors = file_io.read_word_vector(file_path)
    clusters = KMeans(n_clusters=n_clusters, n_init=10, max_iter=300, tol=1e-4)
    print('Training ...')
    clusters.fit(vectors)
    labels = clusters.labels_
    file_io.write_word_vector(words, labels, n_clusters, len(words))
    print('Completed!')


if __name__ == '__main__':
    file_path = './data/popIn_entity_vector.model.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int,
                        help='set the number of clusters')
    parser.add_argument('-p', '--path', type=str,
                        help='path of word vectors')
    args = parser.parse_args()
    n_clusters = args.number
    file_path = args.path
    word_cluster(file_path=file_path, n_clusters=n_clusters)

