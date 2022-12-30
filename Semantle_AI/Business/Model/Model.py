import gensim
from gensim.models import KeyedVectors


class Model:
    def __init__(self, model:KeyedVectors,vocab):
        self.model = model
        self.vocab = vocab

    def get_distance_of_word(self, word1, word2):
        ans = self.model.similarity(word1, word2)
        return ans

    def get_word_from_distance(self, dis: float) -> str:
        pass

    def get_most_similar_by_vec(self, vec):
        return self.model.most_similar(positive = vec,topn=3)

    def get_word_vec(self,word):
        return self.model[word]

    def get_vocab(self):
        return self.vocab
