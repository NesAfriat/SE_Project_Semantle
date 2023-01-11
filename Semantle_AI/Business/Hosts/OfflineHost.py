from random import choice
import math
from Business.Hosts.Host import Host
import Business.ModelFactory as MF

WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"



class OfflineHost(Host):

    def quitGame(self):
        pass

    def __init__(self):
        self.model = None
        self.vocabulary = None
        self.secret_word = None

    def set_host_word2vec_model(self):
        host_model, vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        self.set_model(host_model, vocabulary)

    def set_host_model_from_url(self, name):
        host_model, vocabulary = MF.load_from_gensim(name, WORDS_LIST)
        self.set_model(host_model, vocabulary)

    def get_model(self):
        return self.model

    def set_model(self, model, vocab):
        self.model = model
        self.vocabulary = list(vocab)

    def select_word_and_start_game(self, out):
        out("================ Offline game===============")
        word = choice(list(self.vocabulary))
        self.secret_word = word

    def check_word(self, word):
        if word in self.vocabulary:
            return self.model.get_distance_of_word(self.secret_word, word)
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
