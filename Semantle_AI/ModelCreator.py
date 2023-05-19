import copy
import os
from pathlib import Path
from gensim.models import KeyedVectors
import cProfile
from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Model.Model import Model
import gensim.downloader as api
import Semantle_AI.Business.ModelFactory as mf

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


def save_word_combinations(kv_model, vocabulary, model_name):
    print(f"Word combinations starts for model  {model_name}")
    vocabulary = list(vocabulary)
    output_file = f"{model_name}_{dist_func_name}.txt"
    with open(output_file, 'x') as file:
        for word1 in vocabulary:
            for word2 in vocabulary:
                distance = get_distance_of_word(kv_model, word1, word2)
                line = f"{word1}{word2}${distance:.6f}\n"
                file.write(line)

    print(f"Word combinations and distances saved to {output_file}")