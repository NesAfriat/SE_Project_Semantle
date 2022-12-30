import os.path
from pathlib import Path

import Business.ModelFactory as MF
from Business.GameManager import GameManager


class Play:
    pca = None

    def __init__(self):
        self.game_manager: GameManager = None
        self.finished = False
        self.offline_playing = False

    # starting the menu
    def start_menu(self):
        while not self.finished:
            if self.game_manager == None:
                self.game_manager = GameManager()
            print("menu starting...\n press on 'e' to exit menu any time.\n")
            off_on = self.busy_choose(
                "Choose offline or online Host", "offline.", "online")
            if off_on == '1':
                self.offline_playing = True
                self.game_manager.create_offline_host()
                self.choose_host_model()
            elif off_on == '2':
                self.offline_playing = False
                self.game_manager.create_online_host()
                self.human_or_AI_game()
            elif off_on == 'e':
                self.finished = True
            else:
                print("please choose a valid option")

    # if the choose was for online
    def choose_host_model(self):
        ip = self.busy_choose("Choose Model", "word2vec")
        if ip == 'b':
            self.start_menu()
        elif ip == '1':
            self.game_manager.set_host_word2vec_model()
            self.human_or_AI_game()
        elif ip == 'e':
            self.finished = True

    # choose if u want to play or the agent work..
    def human_or_AI_game(self):
        ip = self.busy_choose(
            "Play against computer or let the agent do the job", "play Manually", "let the agent work")
        if ip == 'b':
            self.choose_host_model()
        elif ip == '1':
            self.start_commandline_game()
        elif ip == '2':
            self.choose_agent()
        elif ip == 'e':
            self.finished = True

    def choose_agent(self):
        def choose_agent_model():
            ip = self.busy_choose(
                "Choose Agent Model", "Word2Vec")
            if ip == 'b':
                self.choose_agent()
            elif ip == '1':
                self.game_manager.create_agent1()
                self.game_manager.create_agent_word2vec_model()
                self.choose_algo()
            elif ip == 'e':
                self.finished = True

        ip = self.busy_choose("Choose Agent", "agent1", "agent2")
        if ip == 'b':
            self.human_or_AI_game()
        elif ip == '1':
            if self.offline_playing:
                self.game_manager.create_agent1()
                self.game_manager.set_agent_host_model()
                self.choose_algo()
            else:
                choose_agent_model()
        elif ip == '2':
            self.game_manager.create_agent2()
            choose_agent_model()
        elif ip == 'e':
            self.finished = True

    def choose_algo(self):
        ip = self.busy_choose("Choose Algorithm", "Naive", "BruteForce", "Trilateraion")
        if ip == 'b':
            self.choose_agent()
        elif ip == '1':
            self.game_manager.set_agent_naive_algorithm()
            self.click_ok_and_start()
        elif ip == '2':
            self.game_manager.set_agent_Brute_Force_algorithm()
            self.click_ok_and_start()
        elif ip == '3':
            self.game_manager.set_agent_trilateration_algorithm()
            self.click_ok_and_start()
        elif ip == 'e':
            self.finished = True

    def busy_choose(self, to_write, *args):
        acc = ""
        num = 1
        for option in args:
            acc = acc + str(num) + ". " + option + "\n"
            num += 1
        num -= 1
        while True:
            ip = input("===================" + to_write + "===================\n\n" + acc)
            if  ip == 'e' or ip == 'b' or (ip.isnumeric() and 0 < int(ip) <= num):
                return ip
            else:
                print("\nplease choose valid option please")

    def click_ok_and_start(self):
        ip = input("\n press enter to start...  \n")
        self.game_manager.start_agent_game(lambda x: print(x))

    def start_commandline_game(self):
        self.game_manager.start_human_game(input, lambda m: print(m))
