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

    def get_number_of_dim(self):
        return self.model.vector_size

    def models_vocab_intersection(self, model2: Model) -> set:
        vocab1 = self.get_vocab()
        vocab2 = model2.get_vocab()
        return vocab1 & vocab2
