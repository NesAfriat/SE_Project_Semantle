from abc import ABC, abstractmethod
from Business import MethodDistances
from Business.Algorithms.MultiLateration import MultiLateration
from Business.Algorithms.Naive import Naive
from Business.Agents.Data import Data
from Business.Algorithms.NLateration import Trilateration
import Business.ModelFactory as MF
from Business.Hosts.OfflineHost import OfflineHost


WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class Agent(ABC):
    def __init__(self):
        self.algorithm = None
        self.host = None
        self.num_og_guesses = 0
        self.init_algo_data = lambda: None
        self.data = Data()
        self.end_score = None
        self.init = None

    @abstractmethod
    def guess_word(self):
        pass

    def set_agent_MultiLateration_algorithm(self):
        algo = MultiLateration(self.data.model.dist_func)
        self.set_algorithm(algo, lambda: self.guess_n_random_word(1))



    def set_agent_naive_algorithm(self):
        algo = Naive()
        self.set_algorithm(algo, lambda: None)

    def set_agent_trilateration_algorithm(self):
        algo = Trilateration()
        self.set_algorithm(algo, lambda: self.guess_n_random_word(self.data.model.get_number_of_dim() + 1))

    def set_end_score(self, end_score):
        self.end_score = end_score

    def set_algorithm(self, algorithm, init_func):
        self.algorithm = algorithm
        self.algorithm.set_data(self.data)
        self.init = init_func

    def set_model(self, model):
        self.data.set_model(model)

    def set_host(self, host):
        self.host = host



    def set_agent_word2vec_model_online(self):
        model, vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        self.set_model(model)
        self.data.model.set_dist_function(MethodDistances.cosine_function())

    def set_agent_model_from_url(self, name):
        agent_model, vocabulary = MF.load_from_gensim(name, WORDS_LIST)
        self.set_model(agent_model)

    def set_agent_word2vec_model(self):
        model, vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        self.set_model(model)
        self.data.model.set_dist_function(MethodDistances.euclid_function())

    # only guess word should be abstract.
    def start_play(self, out):
        self.host.select_word_and_start_game(out)
        self.data.last_score = -2
        self.data.update_statistic()
        self.init()
        while abs(self.data.last_score) != 1.0 and abs(self.data.last_score) != 0:
            try:
                if self.data.last_score == -2:
                    self.guess_random_word()
                else:
                    out(f"Next guessed word:  \'{self.data.last_word}\'. The similarity is:  {str(round(self.data.last_score * 100, 2))}")
                self.add_to_list(self.data.last_word, self.data.last_score)
                word = self.guess_word()
                self.data.last_score = self.host.check_word(word)
                self.data.last_word = word
                self.data.update_statistic()
            except ValueError as e:
                out(e)
                return
        out(f"Last guessed word is: {self.data.last_word}. This is the secret word.")
        out(f"\nGame over.\n"
            f"you won!!\n\n\n\n")

    def add_to_list(self, last_word, dist):
        self.data.add_to_dict(last_word, dist)

    def set_last_score(self, score):
        self.data.last_score = score

    def guess_random_word(self):
        guess = None
        dist = -2
        algo = Naive()
        algo.set_data(self.data)
        while dist == -2:
            if guess is not None:
                self.add_to_list(guess, self.data.last_score)
            guess = algo.calculate()
            dist = self.host.check_word(guess)
        self.data.add_to_dict(guess, dist)

    def guess_n_random_word(self, n):
        for i in range(n):
            self.guess_random_word()
            self.data.update_statistic()

    def inc_num_of_guesses(self):
        self.num_og_guesses = self.num_og_guesses + 1

    def get_model(self):
        return self.data.model

    def get_vocab(self):
        return self.data.remain_words

    def set_secret_word(self, word):
        if self.host is OfflineHost:
            self.host.setWord(word)

    def reset_data(self):
        self.data.reset_vocab()
        self.data.reset()

    def get_statistics(self):
        return self.data.get_statistics()