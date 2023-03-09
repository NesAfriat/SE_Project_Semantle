from abc import ABC, abstractmethod

from Business.Agents import Agent
from Service.HostHandlers.OfflineHostHandler import OfflineHostBuilder
from Service.HostHandlers.OnlineHostBuilder import OnlineHostBuilder
from Service.ModelComparator import ModelComparator

FASTTESXT_WIKI = "fasttext-wiki-news-subwords-300"  # 1GB
GLOVE_WIKI = "glove-wiki-gigaword-300"  # 376MB
WORD2VEC_GOOGLE = "word2vec-google-news-300"  # 1.662GB
WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class AgentHandler(ABC):
    def __init__(self, out, inp, finished):
        self.inp = inp
        self.out = out
        self.finished = finished
        self.agent: Agent = None

    @abstractmethod
    def start_menu(self):
        pass

    def get_result(self):
        return self.agent




    def create_offline_loop_host(self):
        host = OfflineHostBuilder(self.out, self.inp, self.finished)
        host.start_loop_game()
        self.agent.set_host(host.get_result())
        self.on_offline_mode()

    def create_offline_host(self):
        host = OfflineHostBuilder(self.out, self.inp, self.finished)
        host.start_menu()
        self.agent.set_host(host.get_result())
        self.on_offline_mode()

    def create_online_host(self):
        # online on cosine distance
        host = OnlineHostBuilder(self.out, self.inp, self.finished)
        host.start_menu()
        self.agent.set_host(host.get_result())
        self.on_online_mode()

    def busy_choose(self, to_write, *args):
        acc = ""
        num = 1
        for option in args:
            acc = acc + str(num) + ". " + option + "\n"
            num += 1
        num -= 1
        while True:
            ip = self.inp("===================" + to_write + "===================\n\n" + acc)
            if ip == 'e' or ip == 'b' or (ip.isnumeric() and 0 < int(ip) <= num):
                return ip
            else:
                self.out("\nplease choose valid option please")

    def choose_host(self):
        prev_menu = False
        while not self.finished and not prev_menu:
            off_on = self.busy_choose(
                "Choose offline or online Host", "offline.", "online")
            if off_on == '1':
                self.create_offline_host()
            elif off_on == '2':
                self.create_online_host()
            elif off_on == 'e':
                self.finished = True
            prev_menu = True

    def choose_algo(self):
        prev_menu = False
        while not self.finished and not prev_menu:
            ip = self.busy_choose("Choose Algorithm", "Naive", "Multi-Lateration", "n-Lateration")
            if ip == '1':
                self.agent.set_agent_naive_algorithm()
            elif ip == '2':
                self.agent.set_agent_MultiLateration_algorithm()
            elif ip == '3':
                self.agent.set_agent_trilateration_algorithm()
            elif ip == 'e':
                self.finished = True
            # press on b
            prev_menu = True


    def choose_agent_model(self):
        return_prev = False
        while not return_prev and not self.finished:
            ip = self.busy_choose("Choose Agent Model", WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI,
                                  WORD2VEC_GOOGLE)
            if ip == '1':
                self.agent.set_agent_word2vec_model()
            elif ip == '2':
                self.agent.set_agent_model_from_url(FASTTESXT_WIKI)
            elif ip == '3':
                self.agent.set_agent_model_from_url(GLOVE_WIKI)
            elif ip == '4':
                self.agent.set_agent_model_from_url(WORD2VEC_GOOGLE)
            elif ip == 'e':
                self.finished = True
            # pressed b
            return_prev = True

    @abstractmethod
    def on_online_mode(self):
        pass

    @abstractmethod
    def on_offline_mode(self):
        pass


