import random
import time
from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Algorithms.MultiLaterationAgent2 import SmartMultiLateration
from Semantle_AI.Business.Algorithms.MultiLateration import MultiLateration
from Semantle_AI.Business.Algorithms.Naive import Naive
from Semantle_AI.Business.Agents.Data import Data
from Semantle_AI.Business.Algorithms.NLateration import Trilateration
import Semantle_AI.Business.ModelFactory as MF
from Semantle_AI.Business.Hosts.Host import Host

WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class Agent():
    def __init__(self):
        self.algorithm = None
        self.host = None
        self.num_og_guesses = 0
        self.init_algo_data = lambda: None
        self.data = Data()
        self.end_score = None
        self.init = None
        self.id = -1

    def guess_word(self):
        last_word = self.algorithm.calculate()
        return last_word

    def set_host_model(self):
        self.set_model(self.host.model)

    def set_id(self, id):
        self.id = id

    def set_agent_MultiLateration_algorithm(self):
        algo = MultiLateration(self.data.model.dist_func)
        self.set_algorithm(algo, lambda: self.guess_n_random_word(1))

    def set_agent_smart_MultiLateration_algorithm(self):
        algo = SmartMultiLateration(self.data.model.dist_func)
        self.set_algorithm(algo, lambda: self.guess_n_queue_word(1))

    def set_agent_trilateration_algorithm(self):
        algo = Trilateration()
        self.set_algorithm(algo, lambda: self.guess_n_random_word(self.data.model.get_number_of_dim() + 1))

    def set_agent_naive_algorithm(self):
        algo = Naive()
        self.set_algorithm(algo, lambda: None)

    def set_end_score(self, end_score):
        self.end_score = end_score

    def set_algorithm(self, algorithm, init_func):
        self.algorithm = algorithm
        self.algorithm.set_data(self.data)
        self.init = init_func

    def set_model(self, model):
        self.data.set_model(model)

    def set_host(self, host: Host):
        self.host = host

    def set_agent_word2vec_model_online(self):
        model, vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        self.set_model(model)
        self.data.model.set_dist_function(MethodDistances.cosine_function())

    def set_agent_model_from_url(self, name):
        agent_model, vocabulary = MF.load_from_gensim(name, WORDS_LIST)
        vocab = self.host.model.vocab & vocabulary
        agent_model.vocab = vocab
        self.set_model(agent_model)
        self.data.model.set_dist_function(self.host.model.dist_func)

    def set_agent_word2vec_model(self):
        model, vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        self.set_model(model)
        self.data.model.set_dist_function(self.host.model.dist_func)

    # only guess word should be abstract.
    def start_play(self, out):

        if self.data.is_priority:
            self.host.start_game(out)
        else:
            self.host.select_word_and_start_game(out)
            self.data.update_statistic()
            self.data.state.append(self.data.last_word, self.data.last_score)
        print(f"secret word is : {self.host.getWord()}")
        self.data.last_score = -2
        counter = 0
        self.init()
        start_time = time.time()  # get the current time
        self.data.state.append(self.data.last_word, self.data.last_score)
        while abs(self.data.last_score * self.host.error) != 1.0 and abs(self.data.last_score * self.host.error) != 0:
            try:
                if self.data.last_score == -2:
                    self.guess_n_random_word(1)
                else:
                    out(f"Next guessed word:  \'{self.data.last_word}\'. The similarity is:  {str(round(self.data.last_score * 100, 2))}")
                self.add_to_list(self.data.last_word, self.data.last_score)
                word = self.guess_word()
                self.data.last_score = round(self.host.check_word(word), 5)
                self.data.last_word = word
                self.data.update_statistic()
                self.data.state.append(self.data.last_word, self.data.last_score)
                counter += 1
                current_time = time.time()  # get the current time
                elapsed_time = current_time - start_time  # calculate elapsed time
                if elapsed_time >= 60:  # if more than 60 seconds have passed
                    print(f"counter => {counter}")
                    break  # exit the loop
            except ValueError as e:
                out(e)
                return
        out(f"Last guessed word is: {self.data.last_word}. This is the secret word.")
        out(f"\nGame over.\n"
            f"you won!!\n\n\n\n")

    def start_play_with_priority(self, out):
        self.host.select_word_and_start_game(out)
        out(f"secret word is : {self.host.getWord()}")
        self.data.last_score = -2
        self.data.update_statistic()
        self.init()
        counter = 0
        start_time = time.time()  # get the current time
        while abs(self.data.last_score) != 1.0 and abs(self.data.last_score) != 0:
            try:
                if self.data.last_score == -2:
                    self.guess_top_word()
                else:
                    out(f"Next guessed word:  \'{self.data.last_word}\'. The similarity is:  {str(round(self.data.last_score * 100, 2))}")
                self.add_to_list(self.data.last_word, self.data.last_score)
                word = self.guess_word()
                self.data.last_score = round(self.host.check_word(word), 5)
                self.data.last_word = word
                self.data.update_statistic()
                counter += 1
                current_time = time.time()  # get the current time
                elapsed_time = current_time - start_time  # calculate elapsed time

                if elapsed_time > 60:  # if more than 60 seconds have passed
                    print(f"counter => {counter}")
                    break  # exit the loop
            except ValueError as e:
                out(e)
                return
        out(f"Last guessed word is: {self.data.last_word}. This is the secret word.\nYou took "
            f"{len(self.data.statistics)} guesses")
        out(f"you won!!\n\n\n\n")

    def start_manual(self, out):
        self.host.select_word_and_start_game(out)
        out(f"secret word is : {self.host.getWord()}")
        self.data.last_score = -2
        counter = 0
        while self.data.last_score == -2:
            word = self.get_next_word()
            self.data.last_score = round(self.host.check_word(word), 5)
            self.data.last_word = word
        self.data.update_statistic()
        start_time = time.time()  # get the current time
        while abs(self.data.last_score) != 1.0 and abs(self.data.last_score) != 0:
            try:
                out(f"Next guessed word:  \'{self.data.last_word}\'. The similarity is:  {str(round(self.data.last_score * 100, 2))}")
                self.add_to_list(self.data.last_word, self.data.last_score)
                word = self.get_next_word()
                self.data.last_score = round(self.host.check_word(word), 5)
                while self.data.last_score == -2:
                    word = self.get_next_word()
                    self.data.last_score = round(self.host.check_word(word), 5)
                self.data.last_word = word
                self.data.update_statistic()
                counter += 1
                current_time = time.time()  # get the current time
                elapsed_time = current_time - start_time  # calculate elapsed time
                if elapsed_time > 60:  # if more than 60 seconds have passed
                    break  # exit the loop
            except ValueError as e:
                out(e)
                return
        out(f"Last guessed word is: {self.data.last_word}. This is the secret word.\nYou took "
            f"{len(self.data.statistics)} guesses")
        out(f"you won!!\n\n\n\n")

    def add_to_list(self, last_word, dist):
        self.data.add_to_dict(last_word, dist)

    def set_last_score(self, score):
        self.data.last_score = score

    def guess_n_random_word(self, n):
        algo = Naive()
        for i in range(n):
            guess = None
            dist = -2
            algo.set_data(self.data)

            while dist == -2:
                if guess is not None:
                    self.add_to_list(guess, self.data.last_score)
                guess = algo.calculate()
                dist = self.host.check_word(guess)
            self.data.add_to_dict(guess, dist)
            self.data.update_statistic()

    def guess_top_word(self):
        word = random.choice(self.data.words_heap)
        dist = self.host.check_word(word.word)
        self.data.add_to_dict(word.word, dist)
        self.data.last_score = dist
        self.data.last_word = word.word

    def guess_n_queue_word(self, n):
        for i in range(n):
            self.guess_top_word()
            self.data.update_statistic()

    def inc_num_of_guesses(self):
        self.num_og_guesses = self.num_og_guesses + 1

    def get_model(self):
        return self.data.model

    def get_vocab(self):
        return self.data.remain_words

    def set_secret_word(self, word):
        self.host.setWord(word)

    def reset_data(self):
        self.data.reset_vocab()
        self.data.reset()

    def get_statistics(self):
        return self.data.get_statistics()

    @staticmethod
    def get_next_word():
        return input("Insert next guess:\n")

    def with_distance_function(self, dist_func):
        if dist_func == "euclid":
            self.data.model.set_dist_function(MethodDistances.euclid_function())
        else:
            self.data.model.set_dist_function(MethodDistances.cosine_function())
