

def read_word_vector(file_path):
    '''
    param
        file_path: file of word vector file
    return:
        words: list of all words
        vectors: list of all word vectors
    '''

    file = open(file_path)
    line = file.readline().split(' ')
    num_words = int(line[0])
    size_vector = int(line[1])
    print('Number of words: %d, size of vector: %d' %(num_words, size_vector))
    vectors = []
    words = []
    for i in range(num_words):
        if i % int(num_words/10) == 0:
            print('%d%%' % (i*100/num_words))
        line = file.readline().split(' ')
        word = line[0]
        vector = [float(i) for i in line[1:]]
        words.append(word)
        vectors.append(vector)
    file.close()
    return words, vectors


def write_word_vector(words, labels, n_clusters, n_words):
    if len(words) != len(labels):
        print('Numbers of words and labels don\'t match!')
    else:
        file = open('./cluster-%d-%d-words.txt' % (n_clusters, n_words), 'w')
        for i in range(0, len(words)):
            file.write('%d\t%s\n' % (labels[i], words[i]))
        file.close()


if __name__ == '__main__':
    file_path = './data/popIn_entity_vector.model.txt'
    read_word_vector(file_path)
