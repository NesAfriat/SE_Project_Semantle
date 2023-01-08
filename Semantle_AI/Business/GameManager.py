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


        ##set host word2vec model



        # create word2vec for agent only online



        ##set to the agent the same model as the host







    def start_human_game(self, inp, out):
        self.host.select_word_and_start_game(out)
        out("Try to Guess a word!")
        score = -1
        quit = False
        while score != 1.0 and not quit:
            word = inp("-Enter your next word or 0 to return:\n")
            spl = str.split(word, "$")
            if spl[0] == '@':
                self.host.setWord(spl[1])
            elif word != '0':
                score = self.host.check_word(word)
                if score == -2:
                    out("Word is not in the vocabulary, Please try another one.\n")
                else:
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
