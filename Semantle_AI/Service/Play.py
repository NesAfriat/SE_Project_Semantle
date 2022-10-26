import os.path
from pathlib import Path

from Business.GameHost import GameHost
import Business.ModelTrainer as MT
import Business.LoadModel as LM


class Play:

    def __init__(self, vocabulary=[], model=[], host=None):
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
            self.model, self.vocabulary = self.load_model()
            host = GameHost(self.model, self.vocabulary)
            host.select_Word()
            score = -1
            while score != 1:
                word = input("Try to Guess a word: ")
                score = host.check_word(word)
                if score == '-1':
                    print("Word is not in the vocabulary, Please try another words.")
                else:
                    print("The similarity of the words is: ", score)
            print("You won!")
        except ValueError:
            if str(ValueError) == "Train file not found.":
                path_trains = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
                print(f"Train file not found. \nplease add the file in the path: {path_trains}")
                return



    # elif value == '3':
    #     filename = input("\nPlease enter file name, or keep empty for default name.\n")
    #     LM.load_from_file(filename, model, vocabulary)
    # elif value == '4':
    #     filename = input("\nPlease enter file name, or keep empty for default name.\n")
    #     WE.train_new_model(model, filename)
    # elif value == '5':
    #     print("Option not possible yet....")
