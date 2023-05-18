from random import choice
import math
import numpy as np
from Semantle_AI.Business.Hosts.Host import Host
import Semantle_AI.Business.ModelFactory as MF

WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class OfflineHost(Host):

    def quitGame(self):
        pass

    def __init__(self):
        super().__init__()
        self.model = None
        self.vocabulary = None
        self.secret_word = None

    def get_model(self):
        return self.model

    def set_model(self, model, vocab):
        self.model = model
        self.vocabulary = list(vocab)

    def select_word_and_start_game(self, out):
        out("================Offline game===============")
        word = choice(list(self.vocabulary))
        self.secret_word = word

    def start_game(self, out):
        out("================Offline game===============")

    def check_word(self, word):
        if word in self.vocabulary:
            return self.error * self.model.get_distance_of_word(self.secret_word, word)
        return -2

    def set_word(self, new_word):
        self.secret_word = new_word

    def most_similar(self):
        return self.model.get_most_similar(self.secret_word)

    def getWord(self):
        return self.secret_word

    def setWord(self, word):
        self.secret_word = word

    def getWordVec(self, word):
        return self.model.get_word_vec(word)

    def getGuessVec(self, w):
        return self.model.model.distance(w, self.secret_word)

    def getWordsVec(self, w1, w2):
        return np.subtract(self.model.get_word_vec(w1), self.model.get_word_vec(w2))

    def setError(self, err):
        self.error = err
