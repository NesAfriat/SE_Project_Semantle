import random

import gensim
from gensim.models import KeyedVectors


class Model:
    def __init__(self, model: KeyedVectors, vocab):
        self.model = model
        self.vocab = vocab
        self.dist_func = None

    def get_distance_of_word(self, word1, word2):
        ans = self.dist_func(self.model[word1], self.model[word2])
        return ans

    def get_word_from_distance(self, dis: float) -> str:
        pass

    def set_dist_function(self, function):
        self.dist_func = function

    def get_most_similar_by_vec(self, vec):
        return self.model.most_similar(positive=vec, topn=1)

    def get_word_vec(self, word):
        return self.model[word]

    def get_vocab(self):
        return self.vocab
    def get_model(self):
        return self.model

    def get_number_of_dim(self):
        return self.model.vector_size

    def models_vocab_intersection(self, model2) -> set:
        vocab1 = set(self.model.key_to_index)
        vocab2 = set(model2.model.key_to_index)

        return vocab1 & vocab2

    def get_models_error(self, model2, n):
        vocab = self.models_vocab_intersection(model2)
        errors_sum = 0
        error_count = 0
        while error_count < n:
            word1 = random.sample(vocab, 1)[0]
            word2 = random.sample(vocab, 1)[0]
            while word1 == word2:
                word2 = random.sample(vocab, 1)[0]
            dis1 = self.get_distance_of_word(word1, word2)
            dis2 = model2.get_distance_of_word(word1, word2)
            error = abs(dis1-dis2)
            print("error num -", error_count, " is ", error)
            errors_sum += error
            error_count += 1
        return errors_sum/error_count

