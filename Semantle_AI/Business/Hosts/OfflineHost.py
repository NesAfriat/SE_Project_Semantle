from random import choice
import math
from Business.Hosts.Host import Host


class OfflineHost(Host):

    def quitGame(self):
        pass

    def __init__(self):
        self.model = None
        self.vocabulary = None
        self.secret_word = None

    def get_model(self):
        return self.model

    def set_model(self, model, vocab):
        self.model = model
        self.vocabulary = list(vocab)

    def select_word_and_start_game(self, out):
        word = choice(list(self.vocabulary))
        self.secret_word = word

    def check_word(self, word):
        return self.getScore(word)

    def set_word(self, new_word):
        self.secret_word = new_word

    def most_similar(self):
        return self.model.get_most_similar(self.secret_word)

    def getWord(self):
        return self.secret_word

    def setWord(self, word):
        self.secret_word = word
        print(f"new word is {word}")

    def getWordVec(self, word):
        return self.model.get_word_vec(word)

    def getScore(self, word):
        v1 = list(self.getWordVec(word))
        v2 = list(self.getWordVec(self.secret_word))
        return self.getCosSim(v1, v2)

    def getCosSim(self, v1, v2):
        return self.dot(v1, v2) / (self.mag(v1) * self.mag(v2))

    def mag(self, a):
        return math.sqrt(sum(val ** 2 for val in a))

    def dot(self, f1, f2):
        return sum(a * f2[idx] for idx, a in enumerate(f1))
