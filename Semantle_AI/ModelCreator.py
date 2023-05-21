import os

from gensim.models import KeyedVectors

from Semantle_AI.Business import MethodDistances
import Semantle_AI.ModelCreator as mc
import gensim.downloader as api

WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"
dict_model = {0: 'fasttext-wiki-news-subwords-300',
              1: "glove-wiki-gigaword-300",
              2: "word2vec-google-news-300",
              3: "Google_Word2Vec.bin"}

dist_dict = {
    "euclid": MethodDistances.euclid_function(),
    "cosine": MethodDistances.cosine_function()
}

dist_func_name = "cosine"
dist_func = dist_dict[dist_func_name]


def get_distance_of_word(kv_model, w1, w2):
    return dist_func(kv_model[w1], kv_model[w2])


def filter_vocab(vocab, word_list):
    if word_list is None:
        return vocab
    try:
        path = os.path.join(os.getcwd(), "Business", "Model", word_list)
        file = open(path, "r")
        words_set = set((file.read()).split("\n"))
        voc = words_set & vocab
        return voc
    except ValueError as e:
        raise e


def save_word_combinations(kv_model, vocabulary, the_model_name, distance_path, vector_path):
    print(f"Word combinations starts for model  {the_model_name}")
    vocabulary = list(vocabulary)

    # If distance file exists, delete it
    if os.path.isfile(distance_path):
        os.remove(distance_path)

    # If vector file exists, delete it
    if os.path.isfile(vector_path):
        os.remove(vector_path)

    distances_dict = dict()
    vectors_dict = dict()
    with open(distance_path, 'x') as distance_file, open(vector_path, 'x') as vector_file:
        for word1 in vocabulary:
            # Save word vector
            vector = kv_model[word1]
            vectors_dict[word1] = vector
            vector_str = ' '.join(map(str, vector))
            vector_file.write(f"{word1}={vector_str}\n")

            # Save the distance
            for word2 in vocabulary:
                key = f"{word1}{word2}"
                distance = get_distance_of_word(kv_model, word1, word2)
                value = f"{distance:.6f}"
                distances_dict[key] = float(value)
                line = f"{key}${value}\n"
                distance_file.write(line)
    print(f"Word combinations and distances saved to {distance_path} and {vector_path}")
    return distances_dict, vectors_dict


for dist_function_name, dist_function in dist_dict.items():
    for i, model_name in dict_model.items():
        if i == 3:
            # handle from file
            model_path = os.path.join(os.getcwd(), "Business", "Model", model_name)
            # my_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
            # model_vocab = filter_vocab(set(my_model.key_to_index), WORDS_LIST)
            # path = os.path.join(os.getcwd(), "Business", "Model")
            # dist_path = os.path.join(path, f"{model_name}_{dist_function_name}.txt")
            # vec_path = os.path.join(path, f"{model_name}_vectors.txt")
            # distances, vectors = mc.save_word_combinations(my_model, model_vocab, model_name, dist_path, vec_path)

        else:
            path = os.path.join(os.getcwd(), "Business", "Model")
            # dist_path = os.path.join(path, f"{model_name}_{dist_function_name}.txt")
            # vec_path = os.path.join(path, f"{model_name}_vectors.txt")
            # # load from gensim
            # my_model = api.load(model_name)
            # model_vocab = filter_vocab(set(my_model.key_to_index), WORDS_LIST)
            # distances, vectors = mc.save_word_combinations(my_model, model_vocab, model_name, dist_path, vec_path)
