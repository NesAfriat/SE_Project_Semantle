from Business.Host import Host
from Business.WordEmbedding import WordEmbedding
from Service.Play import Play


class Menu:
    def __init__(self, path='C:/Users/nes_afriat/Desktop/Project/SE_Project_Semantle/Semantle_AI/wordtry1.txt'):
        self.path = path

    def play_with_host_only(self):
        word_embedder = WordEmbedding()
        p = Play(word_embedder)
        host = Host()
        p.start_play_with_host_only(host)

    def start_menu(self):
        # switch cases here:#
        value = input("press enter to play with host only")
        self.play_with_host_only()


