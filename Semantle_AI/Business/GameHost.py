import random

from Semantle_AI.Business.Model import Model


class GameHost:
    model = []
    vocabulary = []
    secret_word = ""
    def __init__(self, my_model, vocab):
        self.model = Model(my_model)
        self.vocabulary = vocab
        self.secret_word = None

    def select_Word(self):
        range = len(self.vocabulary)
        word = random.choice(self.vocabulary)
        self.secret_word = word

    def check_word(self, word):
        if word not in self.vocabulary:
            return -1
        else:
            return self.model.get_distance_of_word(self.secret_word, word)