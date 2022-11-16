from random import choice

from Semantle_AI.Business.Model import Model


class OfflineHost:

    def __init__(self):
        self.model = None
        self.vocabulary = None
        self.secret_word = None

    def get_model(self):
        return self.model

    def set_model(self, model,voc):
        self.model = model
        self.vocabulary = voc

    def select_word(self):
        word = choice(self.vocabulary)
        self.secret_word = word

    def check_word(self, word):
        if word not in self.vocabulary:
            return -1
        else:
            return self.model.get_distance_of_word(word, self.secret_word)

    def set_word(self, new_word):
        self.secret_word = new_word

    def in_vocab(self, neww, trained):
        # keyed vector model type
        if trained:
            ans = neww in self.vocabulary
            return ans
        else:
            ans = neww in self.vocabulary
            return ans

    def most_similar(self):
        return self.model.get_most_similar(self.secret_word)
