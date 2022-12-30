import copy
import Business.ModelFactory as MF
from Business import MethodDistances
from Business.Agents.Agent1 import Agent1
from Business.Algorithms.BruteForce import BruteForce
from Business.Algorithms.Naive import Naive
from Business.Algorithms.Trilateration import Trilateration
from Business.Hosts.OfflineHost import OfflineHost
from Business.Hosts.OnlineHost import OnlineHost
import math

from Business.Model.Model import Model


class GameManager:
    WORD2VEC = "Google_Word2Vec.bin"
    WORDS_LIST = "words.txt"

    def __init__(self):
        self.vocabulary = None
        self.trained = None
        self.host = None
        self.agent = None
        self.agent_model: Model = None
        self.host_model: Model = None
        self.dist_formula = None
        self.end_score = None

    def create_offline_host(self):
        self.host = OfflineHost()

    def create_online_host(self):
        self.host = OnlineHost()

        ##set host word2vec model

    def set_host_word2vec_model(self):
        self.host_model, self.vocabulary = MF.load_from_file(self.WORD2VEC, self.WORDS_LIST)
        self.host.set_model(self.host_model, self.vocabulary)

        # create word2vec for agent only online

    def create_agent_word2vec_model_online(self):
        self.agent_model, self.vocabulary = MF.load_from_file(self.WORD2VEC, self.WORDS_LIST)
        self.agent.set_model(self.agent_model)
        self.agent_model.set_dist_function(MethodDistances.cosine_function())

        ##set to the agent the same model as the host

    def set_agent_host_model(self):
        self.agent_model = self.host_model
        self.agent.set_model(self.agent_model)

    def create_agent1(self):
        self.agent = Agent1()
        self.agent.set_host(self.host)
        self.agent.set_end_score(self.end_score)

    def set_euclid_func(self):
        self.dist_formula = MethodDistances.euclid_function()
        self.host_model.set_dist_function(MethodDistances.euclid_function())
        self.end_score = 0

    def set_cosine_function(self):
        self.dist_formula = MethodDistances.cosine_function()
        self.host_model.set_dist_function(MethodDistances.cosine_function())
        self.end_score = 1

    def set_agent_Brute_Force_algorithm(self):
        algo = BruteForce(self.agent_model.dist_func)
        self.agent.set_algorithm(algo, lambda: self.agent.guess_n_random_word(1))

    def set_agent_naive_algorithm(self):
        algo = Naive()
        self.agent.set_algorithm(algo, lambda: None)

    def set_agent_trilateration_algorithm(self):
        algo = Trilateration()
        self.agent.set_algorithm(algo, lambda: self.agent.guess_n_random_word(self.agent_model.get_number_of_dim() + 1))

    def start_human_game(self, inp, out):
        self.host.select_word_and_start_game(out)
        out("==================================================\nTry to Guess a word!")
        score = -1
        quit = False
        while score != 1.0 and not quit:
            word = inp("Enter your next word or 0 to return:\n")
            spl = str.split(word, "$")
            if spl[0] == '@':
                self.host.setWord(spl[1])
            elif word != '0':
                if self.host is OnlineHost:
                    score = self.host.check_word(word)
                else:
                    score = self.host.getScore(word)
                if self.host is OnlineHost:
                    score = score * 100
                out(f"Guessed word is: {str(word)}.\t Similarity is: {str(round(score * 100, 2))} \n")
            else:
                quit = True
        if not quit:
            out("you won!!")
        else:
            out("see you next time!!")
        self.host.quitGame()

    def start_agent_game(self, out):
        self.host.select_word_and_start_game(out)
        self.agent.start_play(out)


def getScore(wordVec, secWordVec):
    return getCosSim(wordVec, secWordVec)


def getCosSim(v1, v2):
    return dot(v1, v2) / (mag(v1) * mag(v2))


def mag(a):
    return math.sqrt(sum(val ** 2 for val in a))


def dot(f1, f2):
    return sum(a * f2[idx] for idx, a in enumerate(f1))
