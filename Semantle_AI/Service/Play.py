import os.path
from pathlib import Path
from decimal import Decimal

from Semantle_AI.Business.GameHost import GameHost
import Semantle_AI.Business.ModelTrainer as MT
import Semantle_AI.Business.LoadModel as LM


class Play:

    pca = None

    def __init__(self):
        pass


    def load_model(self):
        path_model = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/Model.p"
        path_trains = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
        if os.path.isfile(path_model):
            return LM.load_from_file()
        else:
            if os.path.isdir(path_trains):
                return MT.train_new_model()
            else:
                print(">> Unable to create model, Train files are missing.")

                raise Exception("Train file not found.")

    def start_play_with_host_offline(self):
        try:
            self.model, self.vocabulary, self.pca = self.load_model()
            host = GameHost(self.model, self.vocabulary)
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
                score = host.check_word(word)
                if score == '-1':
                    print("Word is not in the vocabulary, Please try another words.")
                else:
                    value = round(score*100, 2)
                    print("The similarity of the words is: ", value)
            print("You won!")
        except ValueError:
            if str(ValueError) == "Train file not found.":
                path_trains = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
                print(f"Train file not found. \nplease add the file in the path: {path_trains}")
                return
