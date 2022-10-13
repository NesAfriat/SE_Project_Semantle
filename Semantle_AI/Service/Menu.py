
from Business.WordEmbedding import WordEmbedding
from Business.Host import Host


class Menu:
    def __init__(self,path='C:/Users/nes_afriat/Desktop/Project/SE_Project_Semantle/Semantle_AI/wordtry1.txt'):
        word_embedder= WordEmbedding()
        host= Host()
        host.init_model(word_embedder,path)
        score=-1
        while score!=1:
            word= input("Try to Guess a word")
            score= host.guess_word_offline(word)
            print("The similarity of the words is: ", score)

        print("You won, fuck you")


