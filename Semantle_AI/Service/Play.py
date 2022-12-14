import os.path
from pathlib import Path

import Business.ModerFactory as MF
from Business.GameManager import GameManager


class Play:
    pca = None

    def __init__(self):
        self.game_manager: GameManager = None

    def load_model(self):
        return MF.load_from_file()

    def start_menu(self):
        self.game_manager = GameManager()
        off_on = input(
            "\n==================================================\n1.Play offline.\n2.Play online.\n3.exit\n")
        if off_on == '1':
            self.game_manager.create_offline_host()
            self.choose_host_model()
        if off_on == '2':
            self.game_manager.create_online_host()
            self.human_or_AI_game()

    # if option 1:
    # this option only in offline
    def choose_host_model(self):
        ip = input("\n b to back \n Choose model: \n 1. word2vec\n")
        if ip == 'b':
            self.start_menu()
        elif ip == '1':
            self.game_manager.set_host_word2vec_model()
            self.human_or_AI_game()

    def human_or_AI_game(self):
        ip = input("\n 1.play Manually \n 2.let the agent work!\n")
        if ip == 'b':
            self.choose_host_model()
        elif ip == '1':
            self.start_commandline_game()
        elif ip == '2':
            self.choose_agent()

    def choose_agent(self):
        ip = input("\n b to back \n Choose model: \n 1. agent1 \n 2. agent2 \n")
        if ip == 'b':
            self.choose_host_model()
        elif ip == '1':
            self.game_manager.create_agent1()
            self.choose_algo()

        elif ip == '2':
            self.game_manager.create_agent2()

    def choose_algo(self):
        ip = input("\n 1.Naive  \n")
        if ip == 'b':
            self.choose_agent()
        elif ip == '1':
            self.game_manager.set_agent_naive_algorithm()
            self.click_ok_and_start()

    def click_ok_and_start(self):
        ip = input("\n enter to start...  \n")
        self.game_manager.start_agent_game(lambda x: print(x))


    def choose_agent_model(self):
        ip = input("\n b to back \n Choose model: \n 1. word2vec\n")
        if ip == 'b':
            self.start_menu()
        elif ip == '1':
            self.game_manager.set_gent_word2vec_model()
            self.human_or_AI_game()


    def start_commandline_game(self):
        self.game_manager.start_human_game(input, lambda m: print(m))

    def choose_model(self):
        ip = input("\n b to back \n Choose model: \n 1. word2vec\n")
        if ip == 'b':
            self.choose_agent()
        # need to initiate model on agent.
        if ip == '1':
            None


"""
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
                        if host.in_vocab(neww, trained):
                            host.setWord(neww)
                            done = True
                            continue
                        else:
                            print(" word is not in the vocabulary, please try another one.")
                            continue
                    if done:
                        done = False
                        continue
                if word == 'most_similar':
                    send = host.most_similar()
                    print("most similar words are:\n ")
                    [print(i[0]) for i in send]
                    print("==================================================")
                    continue
                if word == '0':
                    print("==================================================")
                    return
                if host.in_vocab(word, trained):
                    score = host.check_word(word)
                else:
                    print("Word is not in the vocabulary, Please try another words.")
                    continue
                value = round(score * 100, 2)
                print("The similarity of the words is: ", value)
            print("You won!")
            return self.model, self.vocabulary
        except ValueError:
            if str(ValueError) == "Train file not found.":
                path_trains = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
                print(f"Train file not found. \nplease add the file in the path: {path_trains}")
                return


"""
