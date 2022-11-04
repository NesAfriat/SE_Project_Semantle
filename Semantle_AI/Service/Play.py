import os.path
from pathlib import Path
from decimal import Decimal

from Semantle_AI.Business.GameHost import GameHost
import Semantle_AI.Business.ModelTrainer as MT
import Semantle_AI.Business.LoadModel as LM


class Play:

    pca = None

    def __init__(self, model = None , vocabulary = None):
        self.model = model
        self.vocabulary = vocabulary


    def load_model(self):
        return LM.load_from_file()

    def start_play_with_host_offline(self, trained):
        try:
            if self.model is None:
                self.model, self.vocabulary = self.load_model()
            if self.model is None:
                return
            host = GameHost(self.model)
            host.select_Word()
            score = -1
            print("==================================================\nTry to Guess a word,\npress 0 to exit: ")
            while score != 1:
                word = input("-")
                if word == 'show_word':
                    ans = host.secret_word
                    print(f"The secret word is : {ans}")
                    continue
                if word == 'change_word':
                    done = False
                    while not done:
                        neww = input("Enter the new word:   ")
                        if host.in_vocab(neww):
                            host.setWord(neww)
                            done = True
                        else:
                            print(" word is not in the vocabulary, please try another one.")
                    if done:
                        done = False
                        continue
                if word == '0':
                    print("==================================================")
                    return
                if host.in_vocab(word,trained):
                    score = host.check_word(word)
                else:
                    print("Word is not in the vocabulary, Please try another words.")
                    continue
                value = round(score*100, 2)
                print("The similarity of the words is: ", value)
            print("You won!")
            return self.model, self.vocabulary
        except ValueError:
            if str(ValueError) == "Train file not found.":
                path_trains = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
                print(f"Train file not found. \nplease add the file in the path: {path_trains}")
                return
