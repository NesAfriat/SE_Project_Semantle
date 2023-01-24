from Business import MethodDistances
from Business.Hosts.OfflineHost import OfflineHost
from Service.HostHandlers.HostHandler import HostBuilder
import Business.ModelFactory as MF
from Business.Agents.Agent1 import Agent1
FASTTESXT_WIKI = "fasttext-wiki-news-subwords-300"  # 1GB
GLOVE_WIKI = "glove-wiki-gigaword-300"  # 376MB
WORD2VEC_RUSCORPORA = "word2vec-ruscorpora-300"  # 198MB
WORD2VEC_GOOGLE = "word2vec-google-news-300"  # 1.662GB
WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class OfflineHostBuilder(HostBuilder):

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.host = OfflineHost()

    def start_menu(self):
        self.step_A()

    def start_loop_game(self):
        self.host.set_host_word2vec_model()
        dist_formula = MethodDistances.euclid_function()
        self.host.model.set_dist_function(dist_formula)

    def step_A(self):

        def choose_host_model():
            return_prev = False
            while not return_prev and not self.finished:
                ip = self.busy_choose("Choose Model", "word2vec", FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA,
                                      WORD2VEC_GOOGLE)
                if ip == '1':
                    self.host.set_host_word2vec_model()
                    self.step_B()
                elif ip == '2':
                    self.host.set_host_model_from_url(FASTTESXT_WIKI)
                    self.step_B()
                elif ip == '3':
                    self.host.set_host_model_from_url(GLOVE_WIKI)
                    self.step_B()
                elif ip == '4':
                    self.host.set_host_model_from_url(WORD2VEC_RUSCORPORA)
                    self.step_B()
                elif ip == '5':
                    self.host.set_host_model_from_url(WORD2VEC_GOOGLE)
                    self.step_B()
                elif ip == 'e':
                    self.finished = True
                # pressed b
                return_prev = True

        return choose_host_model()

    def step_B(self):
        def set_euclid_func():
            dist_formula = MethodDistances.euclid_function()
            self.host.model.set_dist_function(dist_formula)

        def set_cosine_func():
            dist_formula = MethodDistances.cosine_function()
            self.host.model.set_dist_function(dist_formula)

        def choose_dist_formula():
            return_prev = False
            while not return_prev and not self.finished:
                ip = self.busy_choose("Choose the semantic distance method", "Euclid", "Cosine")
                if ip == 'b':
                    return_prev = True
                elif ip == '1':
                    set_euclid_func()
                    return_prev = True
                elif ip == '2':
                    set_cosine_func()
                    return_prev = True
                elif ip == 'e':
                    self.finished = True

        return choose_dist_formula()
