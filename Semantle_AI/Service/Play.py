from Business.Host import Host
from Business.WordEmbedding import WordEmbedding


class Play:
    def __init__(self, word_embedder,
                 path='C:/Users/nes_afriat/Desktop/Project/SE_Project_Semantle/Semantle_AI/wordtry1.txt'):
        self.path = path
        self.word_embedder = word_embedder

    def start_play_with_host_only(self, host: Host):
        host.init_model(self.word_embedder, self.path)
        score = -1
        while score != 1:
            word = input("Try to Guess a word")
            score = host.guess_word_offline(word)
            print("The similarity of the words is: ", score)

        print("You won, fuck you")
