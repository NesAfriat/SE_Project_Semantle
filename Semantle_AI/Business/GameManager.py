import copy
import Business.ModelFactory as MF
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

    def create_offline_host(self):
        self.host = OfflineHost()

    def create_online_host(self):
        self.host = OnlineHost()

        ##set host word2vec model

    def set_host_word2vec_model(self):
        self.host_model, self.vocabulary = MF.load_from_file(self.WORD2VEC, self.WORDS_LIST)
        self.host.set_model(self.host_model, self.vocabulary)

        # create word2vec for egent

    def create_agent_word2vec_model(self):
        self.agent_model, self.vocabulary = MF.load_from_file(self.WORD2VEC, self.WORDS_LIST)
        self.agent.set_model(self.agent_model, self.vocabulary)

        ##set to the agent the same model as the host

    def set_agent_host_model(self):
        self.agent_model = self.host_model
        self.agent.set_model(self.agent_model, copy.copy(self.vocabulary))

    def create_agent1(self):
        self.agent = Agent1()
        self.agent.set_host(self.host)


    def set_agent_Brute_Force_algorithm(self):
        algo = BruteForce(lambda words: (self.agent.set_remain_words(words)), self.agent.remain_words,
                          lambda w1, w2: getScore(self.agent_model.get_word_vec(w1), self.agent_model.get_word_vec(w2)))
        self.agent.set_algorithm(algo)

    def set_agent_naive_algorithm(self):
        x = lambda dic: (self.agent.set_remain_words(dic), self.agent.inc_num_of_guesses())
        algo = Naive(x, self.agent.remain_words)
        self.agent.set_algorithm(algo)

    def set_agent_trilateration_algorithm(self):
        algo = Trilateration(lambda: None, self.agent.remain_words)
        self.agent.set_algorithm(algo)

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
                score = None
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
