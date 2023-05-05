from abc import ABC, abstractmethod


WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"



class HostBuilder(ABC):
    def __init__(self, out, inp, finished):
        self.finished = finished
        self.inp = inp
        self.out = out
        self.host = None

    @abstractmethod
    def start_menu(self):
        pass

    def get_result(self):
        return self.host

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
