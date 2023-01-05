from abc import ABC, abstractmethod

from Business.Agents import Agent
import Business.ModelFactory as MF
from Business.Agents.Agent1 import Agent1
from Service.HostMenu.OfflineHostBuilder import OfflineHostBuilder
from Service.HostMenu.OnlineHostBuilder import OnlineHostBuilder

WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class AgentBuilder(ABC):
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

    def create_offline_host(self):
        host = OfflineHostBuilder(self.out, self.inp, self.finished)
        host.start_menu()
        self.agent.set_host(host.get_result())

    def create_online_host(self):
        # online on cosine distance
        host = OnlineHostBuilder(self.out, self.inp, self.finished)
        host.start_menu()
        self.agent.set_host(host.get_result())


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
