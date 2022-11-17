import random
import os.path
from pathlib import Path

import Semantle_AI.Business.ModerFactory as MF
from Semantle_AI.Business.Agents.Agent1 import Agent1
from Semantle_AI.Business.Hosts.OfflineHost import OfflineHost
from Semantle_AI.Business.Model import Model


class GameManager:
    WORD2VEC = "word2vec.wordvectors"

    def __init__(self):
        self.vocabulary = None
        self.trained = None
        self.host = None
        self.agent = None

    def create_offline_host(self):
        self.host = OfflineHost()
        self.agent.set_host(self.host)

    def create_online_host(self):
        pass

    def set_host_word2vec_model(self):
        model, vocabulary = MF.load_from_file(self.WORD2VEC)
        self.host.set_model(model, vocabulary)

    def delete_host(self):
        self.host = None

    def create_word2vec_model(self):
        model, vocabulary, trained = MF.load_from_file(self.WORD2VEC)
        return model, vocabulary

    def create_glove_model(self):
        pass

    def create_agent1(self):
        self.agent.set_model(self.host.get_model())

    def set_agent_algorithm(self):
        self.agent.set_algorithm()

    def select_word(self):
        self.host.select_word()

    def start_human_game(self, inp, out):
        self.host.select_word()
        out("==================================================\nTry to Guess a word,\npress 0 to exit: ")
        score = -1
        while score != 1:
            word = inp("-please guess a word: \n")
            score = self.host.check_word(word)
            if score < 1:
                out("similarity is:" + str(score))
        out("you won!!")

    def start_agent_game(self, out):
        self.host.select_word()
        self.agent.start_play(out)

    def start_AI_game(self):
        pass

    def set_agent1(self):
        pass

    def set_agent2(self):
        pass

    def set_agent3(self):
        pass

    def set_agent_model(self):
        pass
