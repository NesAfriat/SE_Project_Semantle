import random
import os.path
from pathlib import Path

import Business.ModerFactory as MF
from Business.Agents.Agent1 import Agent1
from Business.Agents.Agent2 import Agent2
from Business.Hosts.OfflineHost import OfflineHost
from Business.Hosts.OnlineHost import OnlineHost


class GameManager:
    WORD2VEC = "word2vec.wordvectors"

    def __init__(self):
        self.vocabulary = None
        self.trained = None
        self.host = None
        self.agent = None

    def create_offline_host(self):
        self.host = OfflineHost()


    def create_online_host(self):
        self.host = OnlineHost()

    def set_host_word2vec_model(self):
        model, vocabulary = MF.load_from_file(self.WORD2VEC)
        self.host.set_model(model, vocabulary)

    def set_gent_word2vec_model(self):
        model, vocabulary = MF.load_from_file(self.WORD2VEC)
        self.agent.set_model(model, vocabulary)

    def delete_host(self):
        self.host = None

    def create_word2vec_model(self):
        model, vocabulary, trained = MF.load_from_file(self.WORD2VEC)
        return model, vocabulary

    def create_glove_model(self):
        pass

    def create_agent1(self):
        self.agent = Agent1()
        self.agent.set_host(self.host)
        self.agent.set_model(self.host.get_model())

    def create_agent2(self):
        self.agent = Agent2()
        self.agent.set_host(self.host)

    def setup_agent_model(self, model):
        self.agent = Agent2()
        self.agent.set_host(self.host)
        self.agent.set_model(model)


    def set_agent_algorithm(self):
        self.agent.set_algorithm()

    def select_word(self):
        self.host.select_word_and_start_game()

    def start_human_game(self, inp, out):
        self.host.select_word_and_start_game()
        out("==================================================\nTry to Guess a word,\npress 0 to exit: ")
        score = -1
        while score != 1:
            word = inp("please guess a word: \n")
            score = self.host.check_word(word)
            if score < 1:
                out("similarity is: \n" + str(score))
        self.host.quit()
        out("you won!!")

    def start_agent_game(self, out):
        self.host.select_word_and_start_game()
        self.agent.start_play(out)

    def start_AI_game(self):
        pass

    def set_agent_model(self):
        pass
