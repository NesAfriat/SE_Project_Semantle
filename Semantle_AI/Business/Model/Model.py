import random

import gensim
from gensim.models import KeyedVectors


class Model:
    def __init__(self, distances: dict, vectors: dict, model_vocab: set):
        self.model = vectors
        self.vocab = model_vocab
        self.dist_func = None
        self.distances_dict = distances
        self.error = 1

    def get_distance_of_word(self, word1, word2):
        if len(self.distances_dict) > 0:
            return self.error * self.distances_dict[f"{word1}{word2}"]
        return self.error * self.dist_func(self.model[word1], self.model[word2])

    def setError(self, err):
        self.error = err

    def get_word_from_distance(self, dis: float) -> str:
        pass

    def set_dist_function(self, function):
        self.dist_func = function

    def get_most_similar_by_vec(self, vec):
        try:
            return self.model[vec]
        except:
            return self.model[list(self.vocab)[0]]

    def get_word_vec(self, word):
        try:
            return self.model[word]
        except KeyError as e:
            a = 10
            return []

    def get_vocab(self):
        return self.vocab

    def get_model(self):
        return self.model

    def get_number_of_dim(self):
        return len(self.model[list(self.vocab)[0]])
