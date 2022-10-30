import random
from nltk.corpus import words


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
        word_list = words.words()
        word = random.choice(word_list)
        self.secret_word = word

    def check_word(self, word):
        if word not in self.vocabulary:
            return -1
        else:
            return self.model.get_distance_of_word(self.secret_word, word)

    def setWord(self, neww):
        self.secret_word = neww

    def in_vocab(self, neww):
        return neww in self.vocabulary