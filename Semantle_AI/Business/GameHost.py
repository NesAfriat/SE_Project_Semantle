import random
from nltk.corpus import words

from Semantle_AI.Business.Model import Model


class GameHost:
    model = None
    vocabulary = None
    secret_word = ""

    def __init__(self, my_model):
        self.model = Model(my_model)
        self.vocabulary = list(my_model.index_to_key)
        self.secret_word = None

    def select_Word(self):
        range = len(self.vocabulary)
        word = random.choice(self.vocabulary)
        self.secret_word = word

    def check_word(self, word):
        if word not in self.vocabulary:
            return -1
        else:
            return self.model.get_distance_of_word(word, self.secret_word)

    def setWord(self, neww):
        self.secret_word = neww

    def in_vocab(self, neww, trained):
        # keyed vector model type
        if trained:
            anss = type(self.vocabulary)
            ans = neww in self.vocabulary
            return ans
        else:
            anss = type(self.vocabulary)
            ans = neww in self.vocabulary
            return ans
